from fastapi import FastAPI, Body
import psycopg2
import psycopg2.extras
import re
from datetime import datetime

"""
conn = psycopg2.connect(
    host = input("Database Host:"),
    database = input("Database Name: "),
    user = input("Database User: "),
    password = input("Database Password: "),
)
"""


app = FastAPI()


@app.get('/')
def read_root():
    return {'message': 'Deconnecting API'}


@app.post('/getLocationListing')
def get_location_listing(payload: dict = Body(...)):
    operation = payload.get('operation') 
    location = payload.get('location')  
    budget = int(payload.get('budget'))  
    tripStartDate = payload.get('tripStartDate')  
    tripEndDate = payload.get('tripEndDate')  
    tripStartTime = payload.get('tripStartTime')  
    tripEndTime = payload.get('tripEndTime')  
    totalTripHours = int(payload.get('totalTripHours'))  
    modesNotAllowed = payload.get('modesOfTransport')  
  
    locationGeonameId = int(findSimilarStringSQL("locations", location, "name")[0])
    locationClusterId = int(findSimilarValueinList("clusters", locationGeonameId, "location_id_list")[0])
    possibleRoutes = findRouteswithFilters("routes", locationClusterId, totalTripHours*3600, budget, modesNotAllowed)
    uniqueClusterIds = findUniqueClusterIds(possibleRoutes, locationClusterId)
    uniqueLocations, clusterToLocations = findLocationsFromClusters("clusters", uniqueClusterIds, "cluster_id", "location_id_list")
    possibleLocations = filterLocations("locations", uniqueLocations, "geoname_id", "lowest_hotel_price", tripStartDate, tripEndDate, budget)
    possibleLocationsWithAttractions = findLocationAttractions("attractions",possibleLocations)
    result = {    
        'locations': possibleLocationsWithAttractions,
        'routes': possibleRoutes,
        'clusterKey': clusterToLocations,
    }  
    return result  
  
def findSimilarStringSQL(tableName,searchQuery,coloumn): 
    querySQL = f"""  
            CREATE EXTENSION IF NOT EXISTS pg_trgm; 
            SELECT *  
            FROM {tableName}  
            ORDER BY SIMILARITY(LOWER({coloumn}), LOWER(%s)) DESC
            LIMIT 1;  
        """  
  
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(querySQL,(searchQuery,))  
    result = cur.fetchone()  
    cur.close()  
  
    return result  
  
def findSimilarValueinList(tableName,searchQuery,coloumn): 
    querySQL = f"""  
            SELECT *  
            FROM {tableName}  
            WHERE {searchQuery} = ANY({coloumn}) 
            LIMIT 1;  
        """  
    cur = conn.cursor()  
    cur.execute(querySQL)  
    result = cur.fetchone()  
    cur.close()  
  
    return result  
  
def findRouteswithFilters(tableName, searchQuery, totalTripSeconds, budget, modesNotAllowed):
    modesOfTransport = '|'.join(map(re.escape, modesNotAllowed))
    querySQL = f"""  
            SELECT *  
            FROM {tableName}  
            WHERE (cluster_id_1 = {searchQuery} OR cluster_id_2 = {searchQuery})
            AND time * 2 < {totalTripSeconds} 
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
            if cluster_id_1 not in uniqueClusterIds or cost[0] < uniqueClusterIds[cluster_id_1]:
                uniqueClusterIds[cluster_id_1] = cost[0]  
                
        if cluster_id_2 != locationClusterId:  
            if cluster_id_2 not in uniqueClusterIds or cost[0] < uniqueClusterIds[cluster_id_2]:
                uniqueClusterIds[cluster_id_2] = cost[0]
    
    return uniqueClusterIds  

def findLocationsFromClusters(tableName, searchQuery, coloumn, value):
    uniqueLocations = []
    clusterToLocations = {}

    for cluster_id, lowest_cost in searchQuery.items():
        querySQL = f"""
                SELECT {value}
                FROM {tableName}
                WHERE {coloumn} = {cluster_id};
            """
        cur = conn.cursor()
        cur.execute(querySQL)
        results =  cur.fetchall()
        for result in results:
            for location in result[0]:
                uniqueLocations.append([location, lowest_cost])
        locations = [result[0] for result in results]
        clusterToLocations[cluster_id] = locations

    return uniqueLocations, clusterToLocations

def filterLocations(tableName, searchQuery, coloumn, value, tripStartDate, tripEndDate, budget):
    startDate = datetime.strptime(tripStartDate, '%Y-%m-%d')
    endDate = datetime.strptime(tripEndDate, '%Y-%m-%d')
    totalDays = (startDate - endDate).days
    
    possibleLocations = []

    for location in searchQuery:
        locationId, cost = location
        budgetLeft = int(budget) - cost
        querySQL = f"""
                SELECT * 
                FROM {tableName}
                WHERE {coloumn} = {locationId}
                AND {value} * {totalDays} < {budgetLeft};
            """
        cur = conn.cursor()
        cur.execute(querySQL)
        result = cur.fetchall()

        if result:
            possibleLocations.extend(result)

    return possibleLocations

def findLocationAttractions(tableName, searchQuery):
    for location in searchQuery:
        latitude, longitude = location[2], location[3]
        querySQL = f"""
                SELECT *, 
                point(longitude, latitude) <-> point({longitude}, {latitude}) AS distance
                FROM {tableName}
                ORDER BY point(longitude, latitude) <-> point({longitude}, {latitude})
                LIMIT 10;
        """
        cur =  conn.cursor()
        cur.execute(querySQL)
        results = cur.fetchall()

        if isinstance(location, tuple):
            location = list(location)

        location.append(results)

    return searchQuery
