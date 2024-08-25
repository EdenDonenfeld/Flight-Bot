from Server.database.functions import order_ticket, refund_ticket, change_date, change_dest, check_status, search_flights, get_tickets

def action_by_intent(predicted_label, entities, uid):
    if predicted_label == 0:
        if entities['Date2'] == None:
            print("one way")
            flights = get_flights_one_way(entities)
            if flights == None:
                flights = []
        else:
            print("round trip")
            flights1, flights2 = get_flights_round_trip(entities)
            # if one way flight is not found, set the entire trip to None
            if flights1 == None or flights2 == None:
                flights1 = []
                flights2 = []
            else:
                flights = [flights1, flights2]
        return flights
    elif predicted_label == 1:
        # TODO: User wants to refund ticket, search for ticket, and update user and flight seats
        ticket = check_ticket(entities, uid)
        print("found ticket to refund", ticket)
        return ticket

def check_ticket(entities, uid):
    # check if the user has a ticket that matches the entities
    #load the users tickets
    tickets = get_tickets(uid)
    flights = get_flights_one_way(entities)
    for ticket in tickets:
        flight_num = ticket['FlightNumber']
        for flight in flights:
            if flight['FlightNumber'] == flight_num:
                return ticket
    return tickets
    

    

def get_flights_one_way(entities):
    return search_flights(entities['Origin'], entities['Destination'], entities['Date'])

def get_flights_round_trip(entities):
    flight1 = search_flights(entities['Origin'], entities['Destination'], entities['Date'])
    print("flight1", flight1)
    flight2 = search_flights(entities['Destination'], entities['Origin'], entities['Date2'])
    print("flight2", flight2)
    return flight1, flight2

def launch_functions(predicted_label, entities, uid):
    if predicted_label == 0:
        return order_ticket(uid, entities["flight_num"], entities["seats"])
        
    elif predicted_label == 1:
        refund_ticket(uid, entities["ticket_id"])
        return "כרטיס בוטל בהצלחה!"
    elif predicted_label == 2:
        # check status(uid, ticket_id)
        check_status()
    elif predicted_label == 3:
        # change date(uid, ticket_id, new_date, new_seats)
        change_date()
    elif predicted_label == 4:
        # change dest(uid, ticket_id, new_dest, new_seats)
        change_dest()
    elif predicted_label == 5:
        # weather
        pass
    else:
        # what's allowed
        pass