import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from ticket import Ticket
from user import User


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

# def change_date(flight_num, ticket_num, new_date):
#     # make sure the ticket is ordered by the user
#     # Call the data base - change the date of the ticket
#     print("You have changed the date of the ticket for flight number", flight_num, "to", new_date)


# def change_dest(flight_num, ticket_num, new_dest):
#     # make sure the ticket is ordered by the user
#     # Call the data base - change the destination of the ticket
#     print("You have changed the destination of the ticket for flight number", flight_num, "to", new_dest)


def main():
    cred = credentials.Certificate("Server/database/flightbot-credentials.json")
    firebase_admin.initialize_app(cred)
    ticket_id = order_ticket("12345678", "FB4737", ["1A", "1B", "1C"])
    refund_ticket("12345678", ticket_id)


if __name__ == '__main__':
    main()