import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flight import Flight
import datetime
import random

cred = credentials.Certificate("Server/database/flightbot-credentials.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# List of airport codes from your provided cities
APCode = {
    "ישראל": "TLV",
    "יוון": "ATH",
    "תל אביב": "TLV",
    "ניו יורק": "JFK",
    "לוס אנג'לס": "LAX",
    "פריז": "CDG",
    "לונדון": "LHR",
    "ברלין": "TXL",
    "רומא": "FCO",
    "מדריד": "MAD",
    "אמסטרדם": "AMS",
    "פראג": "PRG",
    "בודפשט": "BUD",
    "וינה": "VIE",
    "פרנקפורט": "FRA",
    "מינכן": "MUC",
    "זיריך": "ZRH",
    "קופנהגן": "CPH",
    "אוסלו": "OSL",
    "סטוקהולם": "ARN",
    "הלסינקי": "HEL",
    "ריגה": "RIX",
    "וילנה": "VNO",
    "קייב": "KBP",
    "מוסקבה": "SVO",
    "סנט פטרסבורג": "LED",
    "קראקוב": "KRK",
    "וורשה": "WAW",
    "בוקרשט": "OTP",
    "סופיה": "SOF",
    "זלצבורג": "ZRH",
}

def create_random_flights():
    # Create a list of cities based on APCode values
    cities = list(APCode.values())

    # Define ranges for generating random data
    dates = [datetime.datetime.now() + datetime.timedelta(days=random.randint(1, 365)) for _ in range(100)]
    durations = ['{:02d}:{:02d}'.format(random.randint(1, 12), random.randint(0, 59)) for _ in range(50)]
    prices = [random.randint(200, 1500) for _ in range(50)]
    statuses = ['On Time', 'Delayed', 'Cancelled']
    seats_list = [f'{row}{seat}' for row in range(1, 11) for seat in 'ABCDEF']

    # Generate flights with different parameters
    for i in range(10):
        origin = random.choice(cities)
        destination = random.choice(cities)
        while destination == origin:
            destination = random.choice(cities)
        
        date = random.choice(dates)
        duration = random.choice(durations)
        price = random.choice(prices)
        status = random.choice(statuses)
        
        flight = Flight(
            flight_number=f'FB{random.randint(1000, 9999)}',
            origin=origin,
            destination=destination,
            date=date,
            duration=duration,
            price=str(price),
            status=status,
            seats=seats_list
        )
        flight.save(db)

        # Optionally create a return flight for round trips
        if random.choice([True, False]):
            return_date = date + datetime.timedelta(days=random.randint(1, 14))
            return_flight = Flight(
                flight_number=f'FB{random.randint(1000, 9999)}',
                origin=destination,
                destination=origin,
                date=return_date,
                duration=duration,
                price=str(price),
                status=status,
                seats=seats_list
            )
            return_flight.save(db)


def create_tlv_flights(number_of_flights):
    # Create a list of cities (excluding TLV)
    destinations = list(APCode.values())

    # Define ranges for generating random data
    dates = [datetime.datetime.now() + datetime.timedelta(days=random.randint(1, 365)) for _ in range(100)]
    durations = ['{:02d}:{:02d}'.format(random.randint(1, 12), random.randint(0, 59)) for _ in range(50)]
    prices = [random.randint(200, 1500) for _ in range(50)]
    statuses = ['On Time', 'Delayed', 'Cancelled']
    seats_list = [f'{row}{seat}' for row in range(1, 11) for seat in 'ABCDEF']

    # Generate only round-trip flights from and to TLV
    for i in range(number_of_flights):
        destination = random.choice(destinations)
        date = random.choice(dates)
        duration = random.choice(durations)
        price = random.choice(prices)
        status = random.choice(statuses)
        
        # Outbound flight (TLV to Destination)
        flight = Flight(
            flight_number=f'FB{random.randint(1000, 9999)}',
            origin='TLV',
            destination=destination,
            date=date,
            duration=duration,
            price=str(price),
            status=status,
            seats=seats_list
        )
        flight.save(db)
        
        # Return flight (Destination to TLV)
        return_date = date + datetime.timedelta(days=random.randint(1, 14))
        return_flight = Flight(
            flight_number=f'FB{random.randint(1000, 9999)}',
            origin=destination,
            destination='TLV',
            date=return_date,
            duration=duration,
            price=str(price),
            status=status,
            seats=seats_list
        )
        return_flight.save(db)


create_tlv_flights(50)