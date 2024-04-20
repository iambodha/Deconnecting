from datetime import datetime, timedelta
import json
import requests

class User:
    def __init__(self, location, budget, tripStartDate, tripEndDate, tripStartTime, tripEndTime, modesOfTransport):
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
        return int(hourEntry.upper().replace('H', ''))

    @staticmethod
    def extractModesOfTransport(modesOfTransport):
        return [mode.strip() for mode in modesOfTransport.split(",")]

    def calculateTripTime(self):
        startDate = datetime.strptime(self.tripStartDate, '%Y-%m-%d')
        startHours = startDate + timedelta(hours=self.tripStartTime)
        endDate = datetime.strptime(self.tripEndDate, '%Y-%m-%d')
        endHours = endDate + timedelta(hours=self.tripEndTime)
        totalHours = (endHours - startHours).total_seconds() / 3600
        return round(int(totalHours))

    def createPayload(self):
        return {
            'operation': 'getLocationListing',
            'location': self.location,
            'budget': self.budget,
            'tripStartDate': self.tripStartDate,
            'tripEndDate': self.tripEndDate,
            'tripStartTime': self.tripStartTime,
            'tripEndTime': self.tripEndTime,
            'totalTripHours': self.totalTripTime,
            'modesOfTransport': self.modesOfTransport,
        }
def main():
    location = input('Enter your City/Town: ')
    budget = int(input('Enter your travel budget: '))
    tripStartDate = input('Starting date of your trip(YYYY-MM-DD): ')
    tripStartTime = input('At what time will you leave(0-23h): ')
    tripEndDate = input('Ending date of your trip(YYYY-MM-DD): ')
    tripEndTime = input('At what time will you like to come back(0-23h): ')
    modesOfTransport = input('Which modes of transport do you not want (Car, Train, Plane, Bus) use commas to seprate values: ')
    testUser = User(location, budget, tripStartDate, tripEndDate, tripStartTime, tripEndTime,modesOfTransport)
    response = requests.post("http://localhost:8000/getLocationListing", json=testUser.createPayload())
    print(response.json())

if __name__ == '__main__':
    main()
