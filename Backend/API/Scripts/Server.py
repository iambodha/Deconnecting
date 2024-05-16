import re
from datetime import datetime

import psycopg2
import psycopg2.extras
from fastapi import Body, FastAPI

conn = psycopg2.connect(
    host=input("Database Host:"),
    database=input("Database Name: "),
    user=input("Database User: "),
    password=input("Database Password: "),
)

"""
Command to run in database
CREATE EXTENSION IF NOT EXISTS pg_trgm; 
"""

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Deconnecting API"}


@app.post("/getLocationID")
def get_location_id(payload: dict[str, str] = Body(...)):
    start_location = payload.get("startLocation")
    closest_locations = findGeonameID(start_location)
    location_info_json = {}
    for closest_location in closest_locations:
        name = closest_location[0]
        first_order = closest_location[1]
        second_order = closest_location[2]
        third_order = closest_location[3]
        country = closest_location[4]
        longitude = closest_location[5]
        latitude = closest_location[6]
        geoname_id = closest_location[7]

        location_info = {
            "name": name,
            "first_order": first_order,
            "second_order": second_order,
            "third_order": third_order,
            "country": country,
            "longitude": longitude,
            "latitude": latitude,
            "geoname_id": geoname_id,
        }

        location_info_json[geoname_id] = location_info

    return location_info_json


@app.post("/getPossibleCountries")
def get_preferences():
    return {"uniqueCountries": ["Germany"]}


@app.post("/getLocations")
def get_locations(payload: dict = Body(...)):
    budget = payload.get("budget")
    trip_start_date = payload.get("tripStartDate")
    trip_end_date = payload.get("tripEndDate")
    total_trip_hours = payload.get("totalTripHours")
    start_location = payload.get("startLocation")
    liked_countries = payload.get("likedCountries")
    disliked_countries = payload.get("dislikedCountries")
    maximum_travel_time = payload.get("maximumTravelTime")
    not_allowed_modes = payload.get("notAllowedModes")
    minimum_hotel_rating = payload.get("minimumHotelRating")
    liked_attraction_types = payload.get("likedAttractionTypes")
    minimum_attraction_rating = payload.get("minimumAttractionRating")
    minimum_review_count = payload.get("minimumReviewCount")
    attraction_phone = payload.get("attractionPhone")
    attraction_website = payload.get("attractionWebsite")

    locationClusterId = int(findClusterID(start_location)[0])
    possibleRoutes = findRouteswithFilters(
        locationClusterId, budget, not_allowed_modes, maximum_travel_time * 3600
    )
    uniqueClusterIds = findUniqueClusterIds(possibleRoutes, locationClusterId)
    uniqueLocations, clusterToLocations = findLocationsFromClusters(uniqueClusterIds)
    possibleLocations = filterLocations(
        uniqueLocations,
        trip_start_date,
        trip_end_date,
        budget,
        liked_countries,
        disliked_countries,
        minimum_hotel_rating,
    )
    formatedRoutes = {
        f"{str(route[0])},{str(route[1])}": {
            "name": route[2],
            "time": route[3],
            "modes": route[4],
            "cost": route[5],
            "places": route[6],
        }
        for route in possibleRoutes
    }
    formatedLocations = {
        location[0]: {
            "name": location[1],
            "latitude": location[2],
            "longitude": location[3],
            "first_order": location[4],
            "second_order": location[5],
            "third_order": location[6],
            "country": location[7],
            "hotel_id_list": location[8],
            "lowest_hotel_price": location[9],
            "highest_hotel_rating": location[10],
            "image_list": location[11],
        }
        for location in possibleLocations
    }
    result = {
        "locations": formatedLocations,
        "routes": formatedRoutes,
        "clusterKey": clusterToLocations,
    }
    return result


@app.post("/getHotel")
def get_hotel(payload: dict = Body(...)):
    hotelID = payload.get("hotelID")
    hotelInformation = getHotelInformation(hotelID)
    return {
        "hotelID": hotelInformation[0],
        "name": hotelInformation[1],
        "latitude": hotelInformation[2],
        "longitude": hotelInformation[3],
        "price": hotelInformation[4],
        "rating": hotelInformation[5],
        "description": hotelInformation[6],
    }


@app.post("/getAttractions")
def get_hotel(payload: dict = Body(...)):
    latitude = payload.get("latitude")
    longitude = payload.get("longitude")
    attractionInformation = getNearbyAttractions(latitude, longitude)
    formatedAttractions = {
        attraction[0]: {
            "title": attraction[1],
            "link": attraction[2],
            "category": attraction[3],
            "address": attraction[4],
            "website": attraction[5],
            "phone": attraction[6],
            "plus_code": attraction[7],
            "review_count": attraction[8],
            "review_rating": attraction[9],
            "latitude": attraction[10],
            "longitude": attraction[11],
            "descriptions": attraction[12],
            "images_list": attraction[13],
        }
        for attraction in attractionInformation
    }
    return {
        "attractions": formatedAttractions,
    }


def findGeonameID(locationName):
    querySQL = """
        SELECT name, first_order, second_order, third_order, country, longitude, latitude, geoname_id
        FROM locations
        ORDER BY SIMILARITY(LOWER(name), LOWER(%s)) DESC
        LIMIT 10;
    """

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(querySQL, (locationName,))
    result = cur.fetchall()
    cur.close()

    return result


def findClusterID(locationName):
    querySQL = f"""  
            SELECT *  
            FROM clusters
            WHERE {locationName} = ANY(location_id_list) 
            LIMIT 1;  
        """
    cur = conn.cursor()
    cur.execute(querySQL)
    result = cur.fetchone()
    cur.close()

    return result


def findRouteswithFilters(searchQuery, budget, modesNotAllowed, maximumTravelTime):
    modesOfTransport = "|".join(map(re.escape, modesNotAllowed))
    querySQL = f"""  
            SELECT *  
            FROM routes
            WHERE (cluster_id_1 = {searchQuery} OR cluster_id_2 = {searchQuery})
            AND time * 2 < {maximumTravelTime} 
            AND (cost[1] * 2) < {budget}  
            AND modes !~ '({modesOfTransport})'; 
        """
    cur = conn.cursor()
    cur.execute(querySQL)
    result = cur.fetchall()

    return result


def findUniqueClusterIds(possibleRoutes, locationClusterId):
    uniqueClusterIds = {}

    for route in possibleRoutes:
        cluster_id_1, cluster_id_2, cost = route[0], route[1], route[5]

        if cluster_id_1 != locationClusterId:
            if (
                cluster_id_1 not in uniqueClusterIds
                or cost[0] < uniqueClusterIds[cluster_id_1]
            ):
                uniqueClusterIds[cluster_id_1] = cost[0]

        if cluster_id_2 != locationClusterId:
            if (
                cluster_id_2 not in uniqueClusterIds
                or cost[0] < uniqueClusterIds[cluster_id_2]
            ):
                uniqueClusterIds[cluster_id_2] = cost[0]

    return uniqueClusterIds


def findLocationsFromClusters(searchQuery):
    uniqueLocations = []
    clusterToLocations = {}

    for cluster_id, lowest_cost in searchQuery.items():
        querySQL = f"""
                SELECT location_id_list
                FROM clusters
                WHERE cluster_id = {cluster_id};
            """
        cur = conn.cursor()
        cur.execute(querySQL)
        results = cur.fetchall()
        for result in results:
            for location in result[0]:
                uniqueLocations.append([location, lowest_cost])
        locations = [result[0] for result in results]
        clusterToLocations[cluster_id] = locations

    return uniqueLocations, clusterToLocations


def filterLocations(
    searchQuery,
    tripStartDate,
    tripEndDate,
    budget,
    likedCountries,
    dislikedCountries,
    minimumHotelRating,
):
    startDate = datetime.strptime(tripStartDate, "%Y-%m-%d")
    endDate = datetime.strptime(tripEndDate, "%Y-%m-%d")
    totalDays = (endDate - startDate).days

    possibleLocations = []

    for location in searchQuery:
        locationId, cost = location
        budgetLeft = int(budget) - cost
        liked_countries_condition = " OR ".join(
            [f"country = '{country}'" for country in likedCountries]
        )
        disliked_countries_condition = " AND ".join(
            [f"country != '{country}'" for country in dislikedCountries]
        )
        querySQL = f"""
            SELECT * 
            FROM locations
            WHERE geoname_id = {locationId}
            AND lowest_hotel_price * {totalDays} < {budgetLeft}
            AND highest_hotel_rating > {minimumHotelRating}
            AND ({liked_countries_condition})
            AND ({disliked_countries_condition});
        """
        cur = conn.cursor()
        cur.execute(querySQL)
        result = cur.fetchall()

        if result:
            possibleLocations.extend(result)

    return possibleLocations


def getHotelInformation(hotelID):
    querySQL = f"""  
        SELECT *  
        FROM hotels
        WHERE hotel_id = {hotelID}
        LIMIT 1;  
    """
    cur = conn.cursor()
    cur.execute(querySQL)
    result = cur.fetchone()
    cur.close()

    return result


def getNearbyAttractions(latitude, longitude):
    querySQL = f"""
        SELECT *, 
            point(longitude, latitude) <-> point({longitude}, {latitude}) AS distance
        FROM attractions
        ORDER BY point(longitude, latitude) <-> point({longitude}, {latitude})
        LIMIT 10;
    """
    cur = conn.cursor()
    cur.execute(querySQL)
    results = cur.fetchall()
    return results
