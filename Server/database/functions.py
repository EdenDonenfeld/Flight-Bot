import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from Server.database.ticket import Ticket
from Server.database.user import User
from Server.database.flight import Flight
from datetime import datetime


def order_ticket(user_id: str, flight_num: str, seats: list):
    # Call the data base - remove the seat from the available seats - and add it to the user
    db = firestore.client()

    user_ref = db.collection('Users').document(user_id)
    user = user_ref.get()
    if not user.exists:
        print("User", user_id, "does not exist in the database")
        return

    flight_ref = db.collection('Flights').document(flight_num)
    flight = flight_ref.get().to_dict()
    print(f'Flight {flight_num} : {flight["Seats"]}')

    # check if the seat is available, remove and update the flight
    for seat in seats:
        if seat in flight['Seats']:
            flight['Seats'].remove(seat)
            flight_ref.set(flight)
            print("You have ordered a ticket for flight number", flight_num, "and seat", seat)
        else:
            print("Seat", seat, "is not available for flight number", flight_num)
            return

    print(f'Flight {flight_num} : {flight["Seats"]}')

    # create a ticket object and save it to users database
    ticket = Ticket(flight_number=flight_num, seats=seats)
    ticket_id = ticket.get_ticket_id()
    print(ticket.to_dict())

    user_data = user.to_dict()
    user = User.from_dict(user_data)
    # Add ticket to user and save
    user.add_ticket(db, ticket)

    return ticket_id




def refund_ticket(user_id: str, ticket_id: str):
    # Call the data base - remove the ticket from the user - and add it to the available seats
    db = firestore.client()

    # check if the user exists
    user_ref = db.collection('Users').document(user_id)
    user = user_ref.get()
    if not user.exists:
        print("User", user_id, "does not exist in the database")
        return

    # check if the ticket exists
    user_data = user.to_dict()
    user = User.from_dict(user_data)

    # add the ticket seats to the flight
    ticket_data = user.get_ticket_by_id(ticket_id)
    ticket = Ticket.from_dict(ticket_data)
    flight_num = ticket.get_flight_num()
    
    flight_ref = db.collection('Flights').document(flight_num)
    flight = flight_ref.get().to_dict()
    # return the seats to the flight to their original state (sorted by number and then letter)
    flight['Seats'] += ticket_data['Seats']
    flight['Seats'] = sorted(flight['Seats'], key=lambda x: (int(x[:-1]), x[-1]))
    flight_ref.set(flight)
    print(f'Flight {flight_num} : {flight["Seats"]}')

    flag = user.remove_ticket(db, ticket_id)
    if not flag:
        return
    print("You have refunded the ticket with ID", ticket_id)

def change_date(user_id: str, ticket_id: str, new_date, new_seats: list): 
    # TODO date is datetime obj
    # make sure the ticket is ordered by the user
    # Call the data base - change the date of the ticket

    # check if new_date is a datetime object
    if not isinstance(new_date, datetime):
        print("new_date is not a datetime object")
        return

    db = firestore.client()
    # Check for a flight with the new date
    # If exists, change ticket to this flight

    # Get the User by user_id
    user_ref = db.collection('Users').document(user_id)
    user = user_ref.get()
    user_data = user.to_dict()
    user = User.from_dict(user_data)

    # Get the ticket of the user
    ticket_data = user.get_ticket_by_id(ticket_id)
    ticket = Ticket.from_dict(ticket_data)
    flight_num = ticket.get_flight_num()
    
    flight_ref = db.collection('Flights')
    flight = flight_ref.document(flight_num).get().to_dict()
    flight_destination = flight["Destination"]

    print("Flight Destination: ", flight_destination)
    flight_query = flight_ref.where("Date", "==", new_date).where("Destination", "==", flight_destination).limit(1).get()

    new_ticket_id = None

    if flight_query:
        flight_data = flight_query[0].to_dict()
        # Found flight with new date and destination
        flight_num = flight_data["FlightNumber"]
        # "refund" for the old flight
        refund_ticket(user_id, ticket_id)
        # order for the new flight
        new_ticket_id = order_ticket(user_id, flight_num, new_seats)

    return new_ticket_id



def change_dest(user_id: str, ticket_id: str, new_dest: str, new_seats: list):
    # make sure the ticket is ordered by the user
    # Call the data base - change the destination of the ticket

    db = firestore.client()
    # Check for a flight with the new destination
    # If exists, change ticket to this flight

    # Get the User by user_id
    user_ref = db.collection('Users').document(user_id)
    user = user_ref.get()
    user_data = user.to_dict()
    user = User.from_dict(user_data)

    # Check for a flight with the new destination
    flight_ref = db.collection('Flights').where("Destination", "==", new_dest).limit(1).get()
    
    if not flight_ref:
        print("No flight found with the new destination.")
        return
    
    # Found flight with new destination
    flight_data = flight_ref[0].to_dict()
    flight_num = flight_data["FlightNumber"]
    
    # "refund" for the old flight
    refund_ticket(user_id, ticket_id)
    # order for the new flight
    new_ticket_id = order_ticket(user_id, flight_num, new_seats)
    return new_ticket_id


def check_status(user_id: str, ticket_id: str):
    # Call the data base - check the status of the flight
    db = firestore.client()
    user_ref = db.collection('Users').document(user_id)
    user = user_ref.get()

    if not user.exists:
        print("User", user_id, "does not exist in the database")
        return
    
    user_data = user.to_dict()
    user = User.from_dict(user_data)

    ticket_data = user.get_ticket_by_id(ticket_id)
    ticket = Ticket.from_dict(ticket_data)

    flight_num = ticket.get_flight_num()
    flight_ref = db.collection('Flights').document(flight_num)
    flight = flight_ref.get().to_dict()

    return flight["Status"]


def search_flights(origin: str, destination: str, date: datetime):
    # Call the data base - search for flights
    # date is y/m/d
    # return 3 closest flights, if there's less than 3, return all
    # add flights to the database
    db = firestore.client()
    flights = db.collection('Flights').where("Origin", "==", origin).where("Destination", "==", destination)
    flights_list = flights.get()
    if flights_list is None:
        print("No flights found")
        return None
        
    # Check for flights with the same date or 1 day or 2 days before or after

    # Case 1: Best Case: date is the same, return all possible flights

    date = date.date()

    flights_list_1 = []
    for flight in flights_list:
        flight_data = flight.to_dict()
        flight_date = flight_data["Date"]
        flight_date_converted = flight_date.date()
        if date == flight_date_converted:
            flights_list_1.append(flight_data["FlightNumber"])

    if flights_list_1:
        return flights_list_1
    
    # Case 2: no flight in the same day, date is 1 day before or after
    flights_list_2 = []
    for flight in flights_list:
        flight_data = flight.to_dict()
        flight_date = flight_data["Date"]
        flight_date_converted = flight_date.date()
        difference = abs((date - flight_date_converted).days)
        if difference <= 1:
            flights_list_2.append(flight_data["FlightNumber"])
    
    if len(flights_list_2) > 2:
        # there are 3 or more flights, return all
        return flights_list_2
    
    # Case 3: Worst Case: no flight in the same day or 1 day before or after, date is 2 days before or after
    flights_list_3 = []
    for flight in flights_list:
        flight_data = flight.to_dict()
        flight_date = flight_data["Date"]
        flight_date_converted = flight_date.date()
        difference = abs((date - flight_date_converted).days)
        if difference <= 2:
            flights_list_3.append(flight_data["FlightNumber"])

    if flights_list_3:
        return flights_list_3
        
    return None


def main():
    cred = credentials.Certificate("Server/database/flightbot-credentials.json")
    firebase_admin.initialize_app(cred)

    flights = search_flights("JFK", "LAX", datetime(2024, 5, 12))
    print("1: ", flights)

    flights = search_flights("JFK", "LAX", datetime(2024, 5, 31))
    print("2: ", flights)

    # TODO
    # User id is not random, its extracted from user's authentication firebase db - UID
    # When user is registered, a new empty user object is created with the UID
    # Test change_date and change_dest

    # change_date example :
    ticket_id = order_ticket("12345678", "FB4737", ["1A", "1B", "1C"])
    new_date = datetime(2024, 5, 12, 10, 0, 0)
    new_ticket_id = change_date("12345678", ticket_id, new_date, ["1A", "1B", "1C"])

    # change_dest example :
    ticket_id_2 = order_ticket("87654321", "FB1234", ["1A", "1B"])
    new_dest = "JFK"
    new_ticket_id_2 = change_dest("87654321", ticket_id_2, new_dest, ["1A", "1B"])

    refund_ticket("12345678", new_ticket_id)
    refund_ticket("87654321", new_ticket_id_2)

    # refund_ticket("12345678", "3cb89ff2")
    # refund_ticket("87654321", "5895a24f")

    status = check_status("12345678", "3be7af8c")
    print("Status:", status)


if __name__ == '__main__':
    main()