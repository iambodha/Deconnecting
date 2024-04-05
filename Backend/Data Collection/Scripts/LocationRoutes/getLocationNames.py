import csv
import requests
import os
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed

def process_location_name(args):
    row, headers = args
    location_name = row[0]
    first_order = row[4]
    url = f"https://www.rome2rio.com/api/1.6/Autocomplete?key=jGq3Luw3&query={urllib.parse.quote(location_name+','+first_order)}&languageCode=en"
    headers = {
                'authority': 'www.rome2rio.com',
                'method': 'GET',
                'path': f"/api/1.6/Autocomplete?key=jGq3Luw3&query={urllib.parse.quote(location_name+','+first_order)}&languageCode=en",
                'scheme': 'https',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Language': 'en-GB,en;q=0.9,en-US;q=0.8,en-IN;q=0.7',
                'Cache-Control': 'max-age=0',
                'Cookie': 'uid=DEXXX20240218085339996uydm; gclid=; r2r_campaign=; sp=869086e8-b5a6-4aa4-86fa-ebc8a7d773c9; __gsas=ID=567515f624b021bd:T=1708246423:RT=1708246423:S=ALNI_MbVdiJ0LYdlTYVvkrKLp15nNcoQmA; FCCDCF=%5Bnull%2Cnull%2Cnull%2C%5B%22CP6LNUAP6LNUAEsACCENAnEgAAAAAAAAAACgAAAAAAAA.YAAAAAAAAAA%22%2C%222~~dv.2072.2074.4131.70.2133.89.93.108.122.149.196.2253.2282.2299.259.2316.2357.311.313.323.2373.338.358.2415.2440.415.449.2506.2510.2526.486.494.495.2568.2571.2575.540.574.2624.2642.2645.2657.609.2677.2767.2887.864.2922.2935.2970.2985.981.3053.1029.1048.1051.1092.1095.1097.1126.5231.3188.3217.1201.1205.1211.3272.1268.1276.3331.1301.1344.1365.1415.1423.1449.1451.1570.1577.1598.1651.1716.1735.1753.1765.1810.1870.1878.1889.1958.1967.2010%22%2C%225ED154CE-805E-4597-A240-B801CF92EA13%22%5D%5D; explore_prefetch=disabled; _ga=GA1.2.284823453.1708863418; acquisition_url=/; HpuUserSetting=off; aqid=DEFra20240402193842704ufdd; _sp_id.3ca3=d1874aa7-a2b8-4f54-b344-25fa266baee2.1708246420.15.1712087004.1711481455.d6d9c7ba-a2cc-48ab-9663-85a1d6a0780c.74f539a3-75fc-47a2-93d9-ce8d5f49f0c8.725f2b54-0c7f-4995-914e-80643e4e0a40.1712086718689.295; __cflb=04dToPBBJs7FiZAfXkN293se9esrpQc3WrRQYFN4QU; __cf_bm=RjntUzHB7bAPZVwNzrjtMPR9ajEXA4IJwfK_dUoYEWw-1712300357-1.0.1.1-7F7mNg75BaM4GjSNwdyNF7lwiRgB0bus6.dI3pQNBoWeKM2MIzMlL9_Sxzt8MkAHw0881Sj3gUNUJqyILg1OpQ',
                'Sec-Ch-Ua': '"Microsoft Edge";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
                'Sec-Ch-Ua-Mobile': '?0',
                'Sec-Ch-Ua-Platform': '"Windows"',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0'
            }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        json_data = response.json()
        results = json_data['results']
        if results:
            first_result = results[0]
            canonical_name = first_result['canonicalName']
            new_row = row + [canonical_name]
            return new_row
        other_url = f"https://www.rome2rio.com/api/1.6/Autocomplete?key=jGq3Luw3&query={urllib.parse.quote(location_name)}&languageCode=en"
        repeated_response = requests.get(other_url, headers=headers)
        if repeated_response.status_code == 200:
            repeated_json_data = repeated_response.json()
            repeated_results = repeated_json_data['results']
            if repeated_results:
                repeated_first_result = repeated_results[0]
                repeated_canonical_name = repeated_first_result['canonicalName']
                new_row = row + [repeated_canonical_name]
                return new_row
        else:
            print("No results found for", location_name)
    return row

def process_location_names(csv_input_file, csv_output_file, skipNum):
    with open(csv_input_file, 'r', encoding='utf-8') as input_file:
        reader = csv.reader(input_file)
        headers = next(reader)
        headers.append('urlName')

        with open(csv_output_file, 'w', newline='', encoding='utf-8') as output_file:
            writer = csv.writer(output_file)
            writer.writerow(headers)

        tasks = []
        for i, row in enumerate(reader):
            if i < skipNum:
                continue
            tasks.append((row, headers))

        with ThreadPoolExecutor(max_workers=4) as executor:
            results = [executor.submit(process_location_name, task) for task in tasks]
            for future in as_completed(results):
                new_row = future.result()
                with open(csv_output_file, 'a', newline='', encoding='utf-8') as output_file:
                    writer = csv.writer(output_file)
                    writer.writerow(new_row)
                print(new_row[0], new_row[1])

def main():
    csv_input_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'allData', 'all_clusters_centroids.csv')
    csv_output_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'allData', 'all_clusters_centroids_with_urls.csv')
    skipNum = int(input("Enter the skip number: "))

    process_location_names(csv_input_file, csv_output_file, skipNum)
    print("\033[92mLocation names have been processed successfully.\033[0m")

if __name__ == "__main__":
    main()

    
