import psycopg2
import csv
from collections import OrderedDict

def create_tables(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clusters (
            cluster_id SERIAL PRIMARY KEY,
            latitude FLOAT NOT NULL,
            longitude FLOAT NOT NULL,
            location_id_list INT[]
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS locations (
            geoname_id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            latitude FLOAT NOT NULL,
            longitude FLOAT NOT NULL,
            first_order TEXT NOT NULL,
            second_order TEXT NOT NULL,
            third_order TEXT NOT NULL,
            hotel_id_list INT[]
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS hotels (
            hotel_id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            latitude FLOAT NOT NULL,
            longitude FLOAT NOT NULL,
            price FLOAT NOT NULL,
            rating FLOAT NOT NULL,
            description TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS routes (
            link TEXT PRIMARY KEY,
            cluster_id_1 INT NOT NULL,
            cluster_id_2 INT NOT NULL,
            name TEXT NOT NULL,
            time TEXT NOT NULL,
            modes TEXT NOT NULL,
            cost TEXT NOT NULL
        )
    """)

def load_data(all_locations, all_stays, all_clusters, all_routes):
    location_data = {}
    with open(all_locations, 'r', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            geoname_id = int(row['geonameId'])
            location_data[geoname_id] = {
                'name': row['Name'],
                'latitude': float(row['Latitude']),
                'longitude': float(row['Longitude']),
                'first_order': row['First Order'],
                'second_order': row['Second Order'],
                'third_order': row['Third Order']
            }

    location_hotel_data = {}
    hotel_data = {}
    with open(all_stays, 'r', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            geoname_id = int(row['geonameId'])
            hotels = eval(row['hotels'])
            location_hotel_data[geoname_id] = hotels
            for hotel in hotels:
                if hotel['hotelId'] is None:
                    hotel['hotelId'] = 0
                else:
                    hotel_id = int(hotel['hotelId'])
                if hotel['name'] is None:
                    hotel['name'] = 'Unknown'
                if hotel['description'] is None:
                    hotel['description'] = 'No description available'
                hotel_data[hotel_id] = {
                    'name': hotel['name'],
                    'latitude': hotel['latitude'],
                    'longitude': hotel['longitude'],
                    'price': hotel['grandTotalPrice'],
                    'rating': hotel['overallGuestRating'],
                    'description': hotel['description']
                }

    cluster_data = {}
    with open(all_clusters, 'r', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            cluster_id = int(row['Cluster'])
            latitude = float(row['Latitude'])
            longitude = float(row['Longitude'])
            geoname_id = next((gid for gid, data in location_data.items() if data['latitude'] == latitude and data['longitude'] == longitude), None)
            if geoname_id is not None:
                if cluster_id in cluster_data:
                    cluster_data[cluster_id].add(geoname_id)
                else:
                    cluster_data[cluster_id] = {geoname_id}

    routes = {}
    number_error = 0
    with open(all_routes, 'r', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            try:
                cluster_id_1 = int(row['Cluster_Start'])
                cluster_id_2 = int(row['Cluster_Stop'])
                current_routes = eval(row['Routes'])
                for route in current_routes:
                    if route['Cost'] == None:
                        route['Cost'] = 'Unknown'
                    link = route['Link']
                    time = route['Time']
                    name = route['Route']
                    modes = route['Method of Transport']
                    cost = route['Cost']
                    routes[link] = (cluster_id_1, cluster_id_2, name, time, modes, cost)
            except:
                number_error += 1
    print(number_error)

    hotel_data = OrderedDict(sorted(hotel_data.items()))
    location_data = OrderedDict(sorted(location_data.items()))

    return location_data, location_hotel_data, cluster_data, hotel_data, routes

def insert_data(cursor, location_data, location_hotel_data, cluster_data, hotel_data, routes, all_clusters_centroids):
    for cluster_id, location_ids in cluster_data.items():
        with open(all_clusters_centroids, 'r', encoding='utf-8') as csvfile:
            csvreader = csv.DictReader(csvfile)
            for row in csvreader:
                if int(row['Cluster']) == cluster_id:
                    latitude = float(row['Latitude'])
                    longitude = float(row['Longitude'])
                    cursor.execute("""
                        INSERT INTO clusters (cluster_id, latitude, longitude, location_id_list)
                        VALUES (%s, %s, %s, %s)
                    """, (cluster_id, latitude, longitude, list(location_ids)))
                    break

    for geoname_id, data in location_data.items():
        hotel_ids = [hotel['hotelId'] for hotel in location_hotel_data.get(geoname_id, [])]
        hotel_id_list = [int(hotel_id) if hotel_id is not None else None for hotel_id in hotel_ids]
        cursor.execute("""
            INSERT INTO locations (geoname_id, name, latitude, longitude, first_order, second_order, third_order, hotel_id_list)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (geoname_id, data['name'], data['latitude'], data['longitude'], data['first_order'], data['second_order'], data['third_order'], hotel_id_list))

    for hotel_id, data in hotel_data.items():
        cursor.execute("""
            INSERT INTO hotels (hotel_id, name, latitude, longitude, price, rating, description)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (hotel_id, data['name'], data['latitude'], data['longitude'], data['price'], data['rating'], data['description']))

    for link, data in routes.items():
        cursor.execute("""
            INSERT INTO routes (link, cluster_id_1, cluster_id_2, name, time, modes, cost)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (link, data[0], data[1], data[2], data[3], data[4], data[5]))

def main():
    all_locations = "../../DataCollection/Scripts/allData/all_locations.csv"
    all_stays = "../../DataCollection/Scripts/allData/all_unique_stays.csv"
    all_clusters = "../../DataCollection/Scripts/allData/all_clusters.csv"
    all_routes = "../../DataCollection/Scripts/allData/all_routes.csv"
    all_clusters_centroids = "../../DataCollection/Scripts/allData/all_clusters_centroids.csv"

    host = input("Enter the host: ")
    database = input("Enter the database: ")
    user = input("Enter the PostgreSQL user: ")
    password = input("Enter the password: ")

    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )

    cur = conn.cursor()

    create_tables(cur)
    location_data, location_hotel_data, cluster_data, hotel_data, routes = load_data(all_locations, all_stays, all_clusters, all_routes)
    insert_data(cur, location_data, location_hotel_data, cluster_data, hotel_data, routes, all_clusters_centroids)

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()