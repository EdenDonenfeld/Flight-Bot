from Server.database.functions import order_ticket, refund_ticket, change_date, change_dest, check_status, search_flights, get_tickets

def action_by_intent(predicted_label, entities, uid):
    if predicted_label == 0:
        flights = get_flights(entities)
        if flights == None:
            flights = []
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
    flights = get_flights(entities)
    for ticket in tickets:
        flight_num = ticket['FlightNumber']
        for flight in flights:
            if flight['FlightNumber'] == flight_num:
                return ticket
    return tickets
    

    

def get_flights(entities):
    return search_flights(entities['Origin'], entities['Destination'], entities['Date'])

def launch_functions(predicted_label, entities, uid):
    if predicted_label == 0:
        return order_ticket(uid, entities["flight_num"], entities["seats"])
        
    elif predicted_label == 1:
        refund_ticket(uid, entities["ticket_id"])
        return "כרטיס בוטל בהצלחה"
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