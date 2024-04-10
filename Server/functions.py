from firebase_admin import firestore

def order_ticket(flight_num: str, seats: list) -> bool:
    # Call the data base - remove the seat from the available seats - and add it to the user
    db = firestore.client()
    # get the flight document
    flight_ref = db.collection('Flights').document(flight_num)
    flight = flight_ref.get().to_dict()

    # check if the seat is available
    for seat in seats:
        if seat in flight['seats']:
            # remove the seat from the available seats
            flight['seats'].remove(seat)
            # update the flight document
            flight_ref.set(flight)
            print("You have ordered a ticket for flight number", flight_num, "and seat", seat)
        else:
            print("Seat", seat, "is not available for flight number", flight_num)
            return False
    return True


# def refund_ticket(flight_num, ticket_num):
#     # make sure the ticket is ordered by the user
#     # Call the data base - remove the ticket from the user - and add it to the available seats
#     # print("You have refunded a ticket for flight number", flight_num, "and seat", seat)

# def change_date(flight_num, ticket_num, new_date):
#     # make sure the ticket is ordered by the user
#     # Call the data base - change the date of the ticket
#     print("You have changed the date of the ticket for flight number", flight_num, "to", new_date)

# def change_dest(flight_num, ticket_num, new_dest):
#     # make sure the ticket is ordered by the user
#     # Call the data base - change the destination of the ticket
#     print("You have changed the destination of the ticket for flight number", flight_num, "to", new_dest)