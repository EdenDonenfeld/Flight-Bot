from Server.database.functions import order_ticket, refund_ticket, change_date, change_dest, check_status, search_flights


def get_flights(entities):
    return search_flights(entities['Origin'], entities['Destination'], entities['Date'])

def launch_functions(predicted_label, entities, uid):
    if predicted_label == 0:
        # order ticket(uid, flight_num, seats)
        order_ticket()
    elif predicted_label == 1:
        # refund ticket(uid, ticket_id)
        refund_ticket()
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