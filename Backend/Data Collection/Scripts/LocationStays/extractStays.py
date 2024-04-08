import csv
import requests
from concurrent.futures import ThreadPoolExecutor
import datetime
import os

fieldnames = []

def process_row(row):
    name = row['Name']
    first_order = row['First Order']
    location_id = f"{name}, {first_order}"

    url = "https://www.priceline.com/pws/v0/pcln-graph/?gqlOp=getAllListings"
    headers = {
        "authority": "www.priceline.com",
        "method": "POST",
        "path": "/pws/v0/pcln-graph/?gqlOp=getAllListings",
        "scheme": "https",
        "Accept-Language": "en-GB,en;q=0.9,en-US;q=0.8",
        "Apollographql-Client-Name": "relax",
        "Apollographql-Client-Version": "master-1.1.1232-v3",
        "Cache-Control": "no-cache",
        "Content-Type": "application/json",
        "Cookie": "",
        "Origin": "https://www.priceline.com",
        "Pragma": "no-cache",
        "Referer": "",
        "Sec-Ch-Ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
        "X-Pcln-Search-Source": "appname:relax-pagename:listings-searchtype:ugs"
    }

    current_date = datetime.datetime.now()
    checkin_date = current_date.replace(day=1) + datetime.timedelta(days=32)
    checkin_date = checkin_date.replace(day=1)
    checkout_date = checkin_date.replace(day=2)
    checkin_date_str = checkin_date.strftime("%Y%m%d")
    checkout_date_str = checkout_date.strftime("%Y%m%d")

    payload = {
            "operationName": "getAllListings",
            "variables": {
                "adults": 1,
                "addErrToResponse": True,
                "allInclusive": False,
                "children": [],
                "checkIn": checkin_date_str,
                "checkOut": checkout_date_str,
                "currencyCode": "EUR",
                "dealTypes": "",
                "first": 10000,
                "googleMapStatic": {
                    "size": {
                            "x": 300,
                            "y": 150
                    },
                    "zoomLevel": 8,
                    "hidePins": True
                },
                "imageCount": 5,
                "allowAllInclusiveImageSort": False,
                "imagesOffsetNum": 1,
                "imagesSortBy": {
                    "amenities": []
                },
                "includeHotelContent": True,
                "includePrepaidFeeRates": True,
                "includePSLResponse": True,
                "locationID": location_id,
                "sortBy": "PROXIMITY",
                "offset": 0,
                "productTypes": ["RTL", "SOPQ"],
                "propertyTypeIds": "",
                "roomCount": 1,
                "unlockDeals": True,
                "vipDeals": False,
                "appCode": "DESKTOP",
                "cguid": "2b8b08da80a1366789bca37db4626450",
                "clientIP": "45.87.212.182",
                "metaID": None,
                "partnerCode": None,
                "plfCode": "PCLN",
                "refClickID": "",
                "rID": "DTDIRECT",
                "authToken": None,
                "userCountryCode": "DE"
            },
            "extensions": {
                "persistedQuery": {
                    "version": 1,
                    "sha256Hash": "c4793f391734f72cfe6c030b9578ad337918b44421c7495e21c19767dda0f42a"
                }
            }
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 403:
        print(response.text)

    hotels_list = []
    if response.json().get("data") is not None and response.json()["data"].get("listings") is not None and response.json()["data"]["listings"].get("hotels") is not None:
        for hotel in response.json()["data"]["listings"]["hotels"]:
                hotel_dict = {
                    "grandTotalPrice": hotel["ratesSummary"]["grandTotal"],
                    "overallGuestRating": hotel["overallGuestRating"],
                    "name": hotel["name"],
                    "latitude": hotel["location"]["latitude"],
                    "longitude": hotel["location"]["longitude"],
                    "hotelId": hotel["hotelId"],
                    "description": hotel["description"]
                }
                hotels_list.append(hotel_dict)

    print("\033[92m", len(hotels_list), name, first_order, response.status_code, "\033[0m")
    row['hotels'] = hotels_list
    with open('../allData/all_stays.csv', 'a', newline='', encoding='utf-8') as new_file:
        writer = csv.DictWriter(new_file,fieldnames=fieldnames)
        writer.writerow(row)

def main():
    with open('../allData/all_locations.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        global fieldnames
        fieldnames = reader.fieldnames + ['hotels']

        with open('../allData/all_stays.csv', 'a', newline='', encoding='utf-8') as new_file:
            writer = csv.DictWriter(new_file, fieldnames=fieldnames)
            writer.writeheader()

        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(process_row, row) for row in reader]
            for future in futures:
                future.result()

    print("\033[92mStays have been extracted successfully.\033[0m")


if __name__ == "__main__":
    main()