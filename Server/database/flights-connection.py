# Connection to flightbot firebase database - Flights collection

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flight import Flight
import datetime

cred = credentials.Certificate("Server/database/flightbot-credentials.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
seats_list = [f'{row}{seat}' for row in range(1, 11) for seat in 'ABCDEF']

# Create a flight object
# date is a timestamp object
flight1 = Flight(
    flight_number='FB4737',
    origin='TLV',
    destination='LON',
    date= datetime.datetime(2024, 5, 1, 8, 0, 0),
    duration='05:30',
    price='750',
    status='On Time',
    seats=seats_list  # Generates the seat list programmatically
)

flight2 = Flight(
    flight_number='FB7402',
    origin='TLV',
    destination='JFK',
    date=datetime.datetime(2024, 5, 10, 12, 0, 0),
    duration='11:00',
    price='1200',
    status='On Time',
    seats=seats_list  # Generates the seat list programmatically
)

flight3 = Flight(
    flight_number='FB6492',
    origin='CDG',
    destination='LON',
    date=datetime.datetime(2024, 5, 12, 10, 0, 0),
    duration='02:00',
    price='300',
    status='On Time',
    seats=seats_list  # Generates the seat list programmatically
)

flight4 = Flight(
    flight_number='FB2048',
    origin='TLV',
    destination='CDG',
    date=datetime.datetime(2024, 5, 15, 14, 0, 0),
    duration='04:30',
    price='600',
    status='On Time',
    seats=seats_list  # Generates the seat list programmatically
)

flight5 = Flight(
    flight_number='FB3804',
    origin='TLV',
    destination='DXB',
    date=datetime.datetime(2024, 4, 25, 16, 0, 0),
    duration='03:30',
    price='500',
    status='On Time',
    seats=seats_list  # Generates the seat list programmatically
)

flight6 = Flight(
    flight_number='FB9731',
    origin='BCN',
    destination='MAD',
    date=datetime.datetime(2024, 4, 18, 18, 0, 0),
    duration='01:30',
    price='200',
    status='On Time',
    seats=seats_list  # Generates the seat list programmatically
)

flight7 = Flight(
    flight_number='FB1804',
    origin='TLV',
    destination='MAD',
    date=datetime.datetime(2024, 5, 5, 20, 0, 0),
    duration='05:00',
    price='750',
    status='On Time',
    seats=seats_list  # Generates the seat list programmatically
)

flight8 = Flight(
    flight_number='FB1234',
    origin='JFK',
    destination='LAX',
    date=datetime.datetime(2024, 5, 30, 22, 0, 0),
    duration='05:00',
    price='500',
    status='On Time',
    seats=seats_list  # Generates the seat list programmatically
)

flight9 = Flight(
    flight_number='FB4321',
    origin='TLV',
    destination='LAX',
    date=datetime.datetime(2024, 5, 1, 6, 0, 0),
    duration='15:00',
    price='1500',
    status='On Time',
    seats=seats_list  # Generates the seat list programmatically
)

flight10 = Flight(
    flight_number='FB5678',
    origin='TLV',
    destination='BER',
    date=datetime.datetime(2024, 5, 16, 4, 0, 0),
    duration='04:00',
    price='450',
    status='On Time',
    seats=seats_list  # Generates the seat list programmatically
)

flight11 = Flight(
    flight_number='FB1235',
    origin='JFK',
    destination='LAX',
    date=datetime.datetime(2024, 5, 30, 8, 0, 0),
    duration='05:00',
    price='500',
    status='On Time',
    seats=seats_list  # Generates the seat list programmatically
)


flight12 = Flight(
    flight_number='FB1236',
    origin='JFK',
    destination='LAX',
    date=datetime.datetime(2024, 5, 31, 12, 0, 0),
    duration='05:00',
    price='500',
    status='On Time',
    seats=seats_list  # Generates the seat list programmatically
)


# Save the flight to Firestore
flight1.save(db)
flight2.save(db)
flight3.save(db)
flight4.save(db)
flight5.save(db)
flight6.save(db)
flight7.save(db)
flight8.save(db)
flight9.save(db)
flight10.save(db)
flight11.save(db)
flight12.save(db)