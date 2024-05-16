import json
import time
from datetime import datetime, timedelta

import requests


class User:
    def __init__(
        self,
        location,
        budget,
        tripStartDate,
        tripEndDate,
        tripStartTime,
        tripEndTime,
        modesOfTransport,
    ):
        self.location = location
        self.budget = budget
        self.tripStartDate = tripStartDate
        self.tripEndDate = tripEndDate
        self.tripStartTime = self.formatHour(tripStartTime)
        self.tripEndTime = self.formatHour(tripEndTime)
        self.totalTripTime = self.calculateTripTime()
        self.modesOfTransport = self.extractModesOfTransport(modesOfTransport)

    @staticmethod
    def formatHour(hourEntry):
        return int(hourEntry.upper().replace("H", ""))

    @staticmethod
    def extractModesOfTransport(modesOfTransport):
        return [mode.strip() for mode in modesOfTransport.split(",")]

    def calculateTripTime(self):
        startDate = datetime.strptime(self.tripStartDate, "%Y-%m-%d")
        startHours = startDate + timedelta(hours=self.tripStartTime)
        endDate = datetime.strptime(self.tripEndDate, "%Y-%m-%d")
        endHours = endDate + timedelta(hours=self.tripEndTime)
        totalHours = (endHours - startHours).total_seconds() / 3600
        return round(int(totalHours))

    def createPayload(self):
        return {
            "operation": "getLocationListing",
            "location": self.location,
            "budget": self.budget,
            "tripStartDate": self.tripStartDate,
            "tripEndDate": self.tripEndDate,
            "tripStartTime": self.tripStartTime,
            "tripEndTime": self.tripEndTime,
            "totalTripHours": self.totalTripTime,
            "modesOfTransport": self.modesOfTransport,
        }


def main():
    """
    location = input('Enter your City/Town: ')
    budget = int(input('Enter your travel budget: '))
    tripStartDate = input('Starting date of your trip(YYYY-MM-DD): ')
    tripStartTime = input('At what time will you leave(0-23h): ')
    tripEndDate = input('Ending date of your trip(YYYY-MM-DD): ')
    tripEndTime = input('At what time will you like to come back(0-23h): ')
    modesOfTransport = input('Which modes of transport do you not want (Car, Train, Plane, Bus) use commas to seprate values: ')
    """
    location = "Berlin"
    budget = 800
    tripStartDate = "2024-06-08"
    tripStartTime = "8"
    tripEndDate = "2024-06-10"
    tripEndTime = "8"
    modesOfTransport = "Plane, Car"
    testUser = User(
        location,
        budget,
        tripStartDate,
        tripEndDate,
        tripStartTime,
        tripEndTime,
        modesOfTransport,
    )
    start_time = time.time()
    payloadLocationID = {
        "startLocation": "Berlin",
    }
    payloadGetLocation = {
        "budget": 200,
        "tripStartDate": "2024-06-08",
        "tripEndDate": "2024-06-10",
        "totalTripHours": 48,
        "startLocation": 6547539,
        "likedCountries": ["Germany", "France"],
        "dislikedCountries": ["Italy"],
        "maximumTravelTime": 8,
        "notAllowedModes": ["Aeroplane", "Car"],
        "minimumHotelRating": 7.0,
        "likedAttractionTypes": [
            "Museum",
            "City or town hall",
            "Shopping mall",
            "Canoe & kayak rental service",
        ],
        "minimumAttractionRating": 4.0,
        "minimumReviewCount": 10,
        "attractionPhone": True,
        "attractionWebsite": False,
    }
    payloadGetHotel = {
        "hotelID": 39193,
    }
    payloadGetAttractions = {
        "latitude": 52.3623,
        "longitude": 9.73402,
    }
    responseGetLocationID = requests.post(
        "http://localhost:8000/getLocationID", json=payloadLocationID
    )

    responseGetPossibleCountries = requests.post(
        "http://localhost:8000/getPossibleCountries"
    )
    responseGetLocations = requests.post(
        "http://localhost:8000/getLocations", json=payloadGetLocation
    )
    responseGetHotel = requests.post(
        "http://localhost:8000/getHotel", json=payloadGetHotel
    )
    responseGetAttractions = requests.post(
        "http://localhost:8000/getAttractions", json=payloadGetAttractions
    )
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Response time:", elapsed_time, "seconds")
    with open("responseGetLocationID.txt", "w") as file:
        file.write(responseGetLocationID.text)

    with open("responseGetPossibleCountries.txt", "w") as file:
        file.write(responseGetPossibleCountries.text)

    with open("responseGetLocations.txt", "w") as file:
        file.write(responseGetLocations.text)

    with open("responseGetHotel.txt", "w") as file:
        file.write(responseGetHotel.text)

    with open("responseGetAttractions.txt", "w") as file:
        file.write(responseGetAttractions.text)


if __name__ == "__main__":
    main()
