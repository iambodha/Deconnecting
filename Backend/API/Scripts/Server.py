from fastapi import FastAPI, Body
import psycopg2

conn = psycopg2.connect(
    host = input("Database Host:"),
    database = input("Database Name: "),
    user = input("Database User: "),
    password = input("Database Password: "),
)

app = FastAPI()


@app.get('/')
def read_root():
    return {'message': 'Deconnecting API'}


@app.post('/getLocationListing')
def get_location_listing(payload: dict = Body(...)):
    operation = payload.get('operation')
    location = payload.get('location')
    budget = payload.get('budget')
    tripStartDate = payload.get('tripStartDate')
    tripEndDate = payload.get('tripEndDate')
    tripStartTime = payload.get('tripStartTime')
    tripEndTime = payload.get('tripEndTime')
    totalTripHours = payload.get('totalTripHours')

    result = {
        'locations': [
            {'name': 'Location 1', 'price': 500},
            {'name': 'Location 2', 'price': 800},
            {'name': 'Location 3', 'price': 700},
        ]
    }
    return result

