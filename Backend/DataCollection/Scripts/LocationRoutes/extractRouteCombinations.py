import csv
from concurrent.futures import ThreadPoolExecutor
import requests
import os
import subprocess
import time
import urllib.parse

current_cookie = None
last_call_time = 0

def get_cookie():
    try:
        result = subprocess.run(['node', 'captureHAR.js'], capture_output=True, text=True, check=True)
        captured_output = result.stdout.replace('\n', '')
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        captured_output = None
    return captured_output

def update_cookie_if_needed():
    global current_cookie
    global last_call_time
    current_time = time.time()
    if current_time - last_call_time >= 120:
        last_call_time = current_time
        new_cookie = get_cookie()
        current_cookie = new_cookie
    else:
        time.sleep(15)

def run_selenium_script(url, url_name1, url_name2):
    global current_cookie
    try:
        headers = {
            "authority": "www.rome2rio.com",
            "method": "GET",
            "path": f"/api/1.5/json/search?key=jGq3Luw3&oName={url_name1}&dName={url_name2}&languageCode=en&currencyCode=EUR&uid=DEXXX20240229154106116uydm&aqid=DEXXX20240229154106116uydm&analytics=true&debugFeatures=&debugExperiments=%2C&flags=&groupOperators=true&noAir=false&noPrice=false",
            "scheme": "https",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "no-cache",
            "Cookie": f"{current_cookie}",
            "Pragma": "no-cache",
            "Referer": "https://www.rome2rio.com/map/Reken/Warburg",
            "Sec-Ch-Ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }

        all_routes = []
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            json_data = response.json()
            if 'routes' in json_data:
                for route in json_data['routes']:
                    current_method_of_transport = route['name']
                    canonical_name = route['canonicalName']
                    time = route['duration']
                    indicative_prices = route['indicativePrices']
                    try:
                        if len(indicative_prices) == 1:
                            min_price_low = min(price_info['priceLow'] for price_info in indicative_prices)
                            max_price_high = max(price_info['priceHigh'] for price_info in indicative_prices)
                        elif len(indicative_prices) == 3:
                            min_price_low = min(price_info['price'] for price_info in indicative_prices)
                            max_price_high = max(price_info['price'] for price_info in indicative_prices)
                        else:
                            min_price_low = 0
                            max_price_high = 0
                    except Exception as e:
                        min_price_low = 0
                        max_price_high = 0
                    cost_range = f'€{min_price_low}–{max_price_high}'
                    keywords_mapping = {
                        'drive': 'Car',
                        'train': 'Train',
                        'fly': 'Plane',
                        'bus': 'Bus',
                    }
                    keywords = [keywords_mapping[key] for key in keywords_mapping if key.lower() in current_method_of_transport.lower()]
                    places_indices = route['places']
                    places_names = [json_data['places'][index]['shortName'] for index in places_indices]
                    route_info = {
                        'Link': canonical_name,
                        'Time': time,
                        'Method of Transport': ', '.join(keywords),
                        'Cost': cost_range,
                        'Places': places_names,
                    }
                    all_routes.append(route_info)
        elif response.status_code == 403:
            update_cookie_if_needed()
        else:
            print(response.status_code)
        return all_routes
    except Exception as e:
        print("Error:", e)
        return []

def process_row(row):
    url_name1 = urllib.parse.quote(row['urlName1'])
    url_name2 = urllib.parse.quote(row['urlName2'])
    link = f"https://www.rome2rio.com/api/1.5/json/search?key=jGq3Luw3&oName={url_name1}&dName={url_name2}&languageCode=en&currencyCode=EUR&uid=DEXXX20240229155401474uydm&aqid=DEXXX20240229155401474uydm&analytics=true&debugFeatures=&debugExperiments=%2C&flags=&groupOperators=true&noAir=false&noPrice=false"
    routes = []
    while not routes:
        routes = run_selenium_script(link, url_name1, url_name2)
    row['Routes'] = routes
    cluster_start = row['Cluster_Start']
    cluster_stop = row['Cluster_Stop']
    print("\033[92m" + f"Cluster Numbers: {cluster_start},{cluster_stop}" + "\033[0m")
    with open(output_csv_path, 'a', newline='', encoding='utf-8') as output_csv:
        csv_writer = csv.DictWriter(output_csv, fieldnames=row.keys())
        csv_writer.writerow(row)
    return row

def main():
    global current_cookie
    global last_call_time
    csv_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'allData', 'all_combinations_with_links.csv')
    output_csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'allData', 'all_routes.csv')

    with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        rows = list(csv_reader)
        header = csv_reader.fieldnames + ['Routes']

    if os.path.exists(output_csv_path):
        existing_rows = set()
        with open(output_csv_path, 'r', encoding='utf-8') as output_csv_file:
            output_csv_reader = csv.DictReader(output_csv_file)
            for existing_row in output_csv_reader:
                key = (existing_row['Cluster_Start'], existing_row['Cluster_Stop'])
                existing_rows.add(key)

        rows = [row for row in rows if (row['Cluster_Start'], row['Cluster_Stop']) not in existing_rows]

    else:
        with open(output_csv_path, 'w', newline='', encoding='utf-8') as output_csv:
            csv_writer = csv.DictWriter(output_csv, fieldnames=header)
            csv_writer.writeheader()

    num_rows = len(rows)

    with open(output_csv_path, 'a', newline='', encoding='utf-8') as output_csv:
        with ThreadPoolExecutor() as executor:
            processed_rows = list(executor.map(process_row, rows))

    print("\033[92m" + f"Script completed. Output CSV saved to {output_csv_path}" + "\033[0m")

if __name__ == '__main__':
    main()