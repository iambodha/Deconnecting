from fastapi import FastAPI, Body
import psycopg2
import psycopg2.extras

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

    locationGeonameId = int(findSimilarStringSQL("locations", location, "name")[0])
    locationClusterId = int(findSimilarValueinList("clusters", locationGeonameId, "location_id_list")[0])
    
    result = {
        'locations': locationGeonameId
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
