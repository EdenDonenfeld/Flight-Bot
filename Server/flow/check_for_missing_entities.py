def check_for_missing(Entities, Predicted_label):
    # label 0 - order a ticket
    # label 1 - refund a ticket
    # label 2 - check the status of a ticket
    # label 3 - change the date of a ticket
    # label 4 - change the destination of a ticket

    # label 5 - know the weather of a destination
    # label 6 - know what is allowed in the flight

    # entities = {"Origin": None, "Destination": None, "Date": None, "Date2": None}
    if Predicted_label >= 0 and Predicted_label <= 4:
        if Entities["Origin"] == None:
            Entities["Origin"] = False
        if Entities["Destination"] == None:
            Entities["Destination"] = False
        if Entities["Date"] == None:
            Entities["Date"] = False
    
    if Predicted_label == 3:
        if Entities["Date2"] == None:
            Entities["Date2"] = False