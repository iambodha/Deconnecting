import requests
import json
from tqdm import tqdm
import random
import csv

global username_list

def geonames_query(query, country_code, total_done=0):
    url = "http://api.geonames.org/searchJSON"
    all_responses = []

    while True:
        params = {
            'q': query,
            'country': country_code,
            'featureClass': 'A',
            'continentCode': '',
            'maxRows': 800,
            'startRow': total_done,
            'username': random.choice(username_list),
        }

        response = requests.get(url, params=params)

        if response.status_code != 200:
            print(f"Error: {response.status_code} - Error occurred while querying GeoNames API.")
            print(f"Chosen username: {params['username']}")
            break

        data = response.json()
        if 'geonames' not in data or len(data['geonames']) == 0:
            print("No more results found for the given query.")
            break

        all_responses.extend(data['geonames'])
        total_done += len(data['geonames'])

        if len(data['geonames']) < 800:
            break

    original_query = query
    if len(query.split()) > 3:
        original_query = ' '.join(query.split()[:3])
    filtered_data = [entry for entry in all_responses if entry.get('fcodeName') == original_query]
    return filtered_data

def get_country_locations(country_code, country):
    result_json = []
    query_result_1 = geonames_query('first-order administrative division', country_code)
    
    for order_1 in tqdm(query_result_1, desc="Processing first-order divisions", unit="division"):
        order_1_data = {
            "name": order_1.get("name"),
            "geonameId": order_1.get("geonameId"),
            "lat": order_1.get("lat"),
            "lng": order_1.get("lng"),
            "suborders": []
        }
        
        query_result_2 = geonames_query(f'second-order administrative division {order_1.get("name")}', country_code)
        if len(query_result_2) == 0:
            query_result_2.append(order_1)
            
        for order_2 in tqdm(query_result_2, desc="Processing second-order divisions", unit="division", leave=False):
            order_2_data = {
                "name": order_2.get("name"),
                "geonameId": order_2.get("geonameId"),
                "lat": order_2.get("lat"),
                "lng": order_2.get("lng"),
                "suborders": []
            }
            
            query_result_3 = geonames_query(f'third-order administrative division {order_2.get("name")}', country_code)
            if len(query_result_3) == 0:
                query_result_3.append(order_2)
                
            for order_3 in tqdm(query_result_3, desc="Processing third-order divisions", unit="division", leave=False):
                order_3_data = {
                    "name": order_3.get("name"),
                    "geonameId": order_3.get("geonameId"),
                    "lat": order_3.get("lat"),
                    "lng": order_3.get("lng"),
                    "suborders": []
                }
                
                query_result_4 = geonames_query(f'fourth-order administrative division {order_3.get("name")}', country_code)
                if len(query_result_4) == 0:
                    query_result_4.append(order_3)
                    
                for order_4 in query_result_4:
                    order_4_data = {
                        "name": order_4.get("name"),
                        "geonameId": order_4.get("geonameId"),
                        "lat": order_4.get("lat"),
                        "lng": order_4.get("lng")
                    }
                    order_3_data["suborders"].append(order_4_data)
                
                order_2_data["suborders"].append(order_3_data)
            
            order_1_data["suborders"].append(order_2_data)
        
        result_json.append(order_1_data)
    
    flatten_and_write_to_csv(result_json, f'../allData/{country}_locations.csv')

def flatten_and_write_to_csv(json_data, csv_file_path):
    def flatten_json(json_data, first_order='', second_order='', third_order='', result=[]):
        if json_data is None:
            return result
        if not isinstance(json_data, list):
            print(f"Invalid JSON structure. Expected a list, but got: {json_data}")
            return result
        for item in json_data:
            name = item.get('name', '')
            geonameId = item.get('geonameId', '')
            lat = item.get('lat', '')
            lng = item.get('lng', '')
            if 'suborders' not in item:
                result.append([name, geonameId, lat, lng, first_order, second_order, third_order])
            if 'suborders' in item:
                flatten_json(item['suborders'], second_order, third_order, name, result)
        return result

    def remove_duplicates(lst):
        seen = set()
        unique_list = []
        for item in lst:
            geonameId = item[1]
            if geonameId not in seen:
                unique_list.append(item)
                seen.add(geonameId)
        return unique_list

    flattened_data = flatten_json(json_data)
    print(f"Total number of locations: {len(flattened_data)}")

    flattened_data_no_duplicates = remove_duplicates(flattened_data)
    print(f"Number of unique locations after removing duplicates: {len(flattened_data_no_duplicates)}")

    header = ['Name', 'geonameId', 'Latitude', 'Longitude', 'First Order', 'Second Order', 'Third Order']
    with open(csv_file_path, 'w', newline='',encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(header)
        csv_writer.writerows(flattened_data_no_duplicates)

    print('\033[92m' + f'CSV file created at: {csv_file_path}' + '\033[0m')

def main():
    global username_list

    input_username_list = input("Enter Geoname Account Usernames List: ")
    country_code = input("Enter Country Code: ")
    country = input("Enter Country Name: ")

    filtered_input_username_list = input_username_list.strip('[]')
    filtered_input_username_list = filtered_input_username_list.replace('"', '')
    filtered_input_username_list = filtered_input_username_list.replace("'", '')
    username_list = filtered_input_username_list.split(',')
    username_list = [username.strip() for username in username_list if username.strip()]

    get_country_locations(country_code, country)

if __name__ == "__main__":
    main()