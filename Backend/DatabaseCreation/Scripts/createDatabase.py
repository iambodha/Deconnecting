import csv
import math
from collections import OrderedDict
from itertools import chain

import psycopg2

csv.field_size_limit(2147483647)


def create_tables(cursor):
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS clusters (
            cluster_id SERIAL PRIMARY KEY,
            latitude FLOAT NOT NULL,
            longitude FLOAT NOT NULL,
            location_id_list INT[]
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS locations (
            geoname_id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            latitude FLOAT NOT NULL,
            longitude FLOAT NOT NULL,
            first_order TEXT NOT NULL,
            second_order TEXT NOT NULL,
            third_order TEXT NOT NULL,
            country TEXT NOT NULL,
            hotel_id_list INT[],
            lowest_hotel_price FLOAT NOT NULL,
            highest_hotel_rating FLOAT NOT NULL,
            image_list TEXT[]
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS hotels (
            hotel_id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            latitude FLOAT NOT NULL,
            longitude FLOAT NOT NULL,
            price FLOAT NOT NULL,
            rating FLOAT NOT NULL,
            description TEXT NOT NULL
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS routes (
            cluster_id_1 INT,
            cluster_id_2 INT,
            link TEXT,
            time INT NOT NULL,
            modes TEXT NOT NULL,
            cost INTEGER[],
            places TEXT[],
            PRIMARY KEY (cluster_id_1, cluster_id_2, link)
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS attractions (
            cid NUMERIC PRIMARY KEY,
            title TEXT NOT NULL,
            link TEXT NOT NULL,
            category TEXT NOT NULL,
            address TEXT NOT NULL,
            website TEXT NOT NULL,
            phone TEXT NOT NULL,
            plus_code TEXT NOT NULL,
            review_count INT NOT NULL,
            review_rating FLOAT NOT NULL,
            latitude FLOAT NOT NULL,
            longitude FLOAT NOT NULL,
            descriptions TEXT NOT NULL,
            images_list TEXT[]
        )
    """
    )


def load_data(all_locations, all_stays, all_clusters, all_routes, all_attractions):
    location_data = {}
    with open(all_locations, "r", encoding="utf-8") as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            geoname_id = int(row["geonameId"])
            location_data[geoname_id] = {
                "name": row["Name"],
                "latitude": float(row["Latitude"]),
                "longitude": float(row["Longitude"]),
                "first_order": row["First Order"],
                "second_order": row["Second Order"],
                "third_order": row["Third Order"],
                "country": row["Country"],
            }

    location_hotel_data = {}
    hotel_data = {}
    with open(all_stays, "r", encoding="utf-8") as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            geoname_id = int(row["geonameId"])
            hotels = eval(row["hotels"])
            location_hotel_data[geoname_id] = hotels
            for hotel in hotels:
                if hotel["hotelId"] is None:
                    hotel["hotelId"] = 0
                else:
                    hotel_id = int(hotel["hotelId"])
                if hotel["name"] is None:
                    hotel["name"] = "Unknown"
                if hotel["description"] is None:
                    hotel["description"] = "No description available"
                hotel_data[hotel_id] = {
                    "name": hotel["name"],
                    "latitude": hotel["latitude"],
                    "longitude": hotel["longitude"],
                    "price": hotel["grandTotalPrice"],
                    "rating": hotel["overallGuestRating"],
                    "description": hotel["description"],
                }

    cluster_data = {}
    with open(all_clusters, "r", encoding="utf-8") as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            cluster_id = int(row["Cluster"])
            latitude = float(row["Latitude"])
            longitude = float(row["Longitude"])
            geoname_id = next(
                (
                    gid
                    for gid, data in location_data.items()
                    if data["latitude"] == latitude and data["longitude"] == longitude
                ),
                None,
            )
            if geoname_id is not None:
                if cluster_id in cluster_data:
                    cluster_data[cluster_id].add(geoname_id)
                else:
                    cluster_data[cluster_id] = {geoname_id}

    routes = {}
    number_error = 0
    with open(all_routes, "r", encoding="utf-8") as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            try:
                cluster_id_1 = int(row["Cluster_Start"])
                cluster_id_2 = int(row["Cluster_Stop"])
                current_routes = eval(row["Routes"])
                for route in current_routes:
                    if isinstance(route["Cost"], str):
                        cost_range = route["Cost"].replace("€", "").split("–")
                        cost = [int(cost.strip()) for cost in cost_range]
                    else:
                        cost = None
                    link = route["Link"]
                    time = int(route["Time"])
                    modes = route["Method of Transport"]
                    places = route["Places"]
                    routes[(cluster_id_1, cluster_id_2, link)] = (
                        time,
                        modes,
                        cost,
                        places,
                    )
            except:
                number_error += 1
    print(number_error)

    hotel_data = OrderedDict(sorted(hotel_data.items()))
    location_data = OrderedDict(sorted(location_data.items()))

    attractions = {}
    with open(all_attractions, "r", encoding="utf-8") as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            cid = int(row["cid"])
            title = row["title"]
            link = row["link"]
            category = row["category"]
            address = row["address"]
            website = row["website"]
            phone = row["phone"]
            plus_code = row["plus_code"]
            review_count = int(row["review_count"])
            review_rating = float(row["review_rating"])
            latitude = float(row["latitude"])
            longitude = float(row["longitude"])
            descriptions = row["descriptions"]
            images_list = eval(row["images"])
            attractions[cid] = {
                "title": title,
                "link": link,
                "category": category,
                "address": address,
                "website": website,
                "phone": phone,
                "plus_code": plus_code,
                "review_count": review_count,
                "review_rating": review_rating,
                "latitude": latitude,
                "longitude": longitude,
                "descriptions": descriptions,
                "images_list": images_list,
            }

    return (
        location_data,
        location_hotel_data,
        cluster_data,
        hotel_data,
        routes,
        attractions,
    )


def insert_data(
    cursor,
    location_data,
    location_hotel_data,
    cluster_data,
    hotel_data,
    routes,
    attractions,
    all_clusters_centroids,
):
    for cluster_id, location_ids in cluster_data.items():
        with open(all_clusters_centroids, "r", encoding="utf-8") as csvfile:
            csvreader = csv.DictReader(csvfile)
            for row in csvreader:
                if int(row["Cluster"]) == cluster_id:
                    latitude = float(row["Latitude"])
                    longitude = float(row["Longitude"])
                    cursor.execute(
                        """
                        INSERT INTO clusters (cluster_id, latitude, longitude, location_id_list)
                        VALUES (%s, %s, %s, %s)
                    """,
                        (cluster_id, latitude, longitude, list(location_ids)),
                    )
                    break

    for geoname_id, data in location_data.items():
        hotel_ids = [
            hotel["hotelId"] for hotel in location_hotel_data.get(geoname_id, [])
        ]
        hotel_id_list = [
            int(hotel_id) if hotel_id is not None else None for hotel_id in hotel_ids
        ]

        hotel_prices = [
            hotel_data[hotel_id]["price"]
            for hotel_id in hotel_id_list
            if hotel_id in hotel_data
        ]
        lowest_hotel_price = min(hotel_prices) if hotel_prices else 0.0

        hotel_ratings = [
            hotel_data[hotel_id]["rating"]
            for hotel_id in hotel_id_list
            if hotel_id in hotel_data
        ]
        highest_hotel_rating = max(hotel_ratings) if hotel_ratings else 0.0

        cursor.execute(
            """
            INSERT INTO locations (geoname_id, name, latitude, longitude, first_order, second_order, third_order, country, hotel_id_list, lowest_hotel_price, highest_hotel_rating)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                geoname_id,
                data["name"],
                data["latitude"],
                data["longitude"],
                data["first_order"],
                data["second_order"],
                data["third_order"],
                data["country"],
                hotel_id_list,
                lowest_hotel_price,
                highest_hotel_rating,
            ),
        )

    for hotel_id, data in hotel_data.items():
        cursor.execute(
            """
            INSERT INTO hotels (hotel_id, name, latitude, longitude, price, rating, description)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
            (
                hotel_id,
                data["name"],
                data["latitude"],
                data["longitude"],
                data["price"],
                data["rating"],
                data["description"],
            ),
        )

    for (cluster_id_1, cluster_id_2, link), data in routes.items():
        time, modes, cost, places = data
        cursor.execute(
            """
            INSERT INTO routes (cluster_id_1, cluster_id_2, link, time, modes, cost, places)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
            (cluster_id_1, cluster_id_2, link, time, modes, cost, places),
        )

    for cid, data in attractions.items():
        cursor.execute(
            """
            INSERT INTO attractions (cid, title, link, category, address, website, phone, plus_code, review_count, review_rating, latitude, longitude, descriptions, images_list)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
            (
                cid,
                data["title"],
                data["link"],
                data["category"],
                data["address"],
                data["website"],
                data["phone"],
                data["plus_code"],
                data["review_count"],
                data["review_rating"],
                data["latitude"],
                data["longitude"],
                data["descriptions"],
                data["images_list"],
            ),
        )


def findLocationAttractions(tableName, location, cur):
    latitude, longitude = location[2], location[3]
    querySQL = f"""
        SELECT images_list, 
            point(longitude, latitude) <-> point({longitude}, {latitude}) AS distance
        FROM {tableName}
        ORDER BY point(longitude, latitude) <-> point({longitude}, {latitude})
        LIMIT 10;
    """
    cur.execute(querySQL)
    results = cur.fetchall()
    return results


def update_location_image_list(cursor):
    cursor.execute(
        """
        SELECT geoname_id, name, latitude, longitude
        FROM locations
        ORDER BY geoname_id
    """
    )
    locations = cursor.fetchall()

    for location in locations:
        location_with_attractions = findLocationAttractions(
            "attractions", location, cursor
        )
        allAttractions = []
        for attraction in location_with_attractions:
            allAttractions.extend(attraction[0])

        geoname_id = location[0]
        cursor.execute(
            """
            UPDATE locations
            SET image_list = %s
            WHERE geoname_id = %s
            """,
            (allAttractions, geoname_id),
        )


def main():
    all_locations = "../../DataCollection/Scripts/allData/all_locations.csv"
    all_stays = "../../DataCollection/Scripts/allData/all_unique_stays.csv"
    all_clusters = "../../DataCollection/Scripts/allData/all_clusters.csv"
    all_routes = "../../DataCollection/Scripts/allData/all_routes.csv"
    all_clusters_centroids = (
        "../../DataCollection/Scripts/allData/all_clusters_centroids.csv"
    )
    all_attractions = "../../DataCollection/Scripts/allData/all_attractions.csv"

    host = input("Enter the host: ")
    database = input("Enter the database: ")
    user = input("Enter the PostgreSQL user: ")
    password = input("Enter the password: ")

    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password,
        options="-c client_encoding=utf8",
    )

    cur = conn.cursor()

    create_tables(cur)
    (
        location_data,
        location_hotel_data,
        cluster_data,
        hotel_data,
        routes,
        attractions,
    ) = load_data(all_locations, all_stays, all_clusters, all_routes, all_attractions)
    insert_data(
        cur,
        location_data,
        location_hotel_data,
        cluster_data,
        hotel_data,
        routes,
        attractions,
        all_clusters_centroids,
    )

    conn.commit()

    update_location_image_list(cur)
    conn.commit()
    cur.close()
    conn.close()
    print("\033[92mDatabase created successfully\033[0m")


if __name__ == "__main__":
    main()
