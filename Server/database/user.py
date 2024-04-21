class User:
    def __init__(self, user_id, tickets=[]):
        self.user_id = user_id
        self.tickets = tickets

    def to_dict(self):
        return {
            'UserID': self.user_id,
            'Tickets': self.tickets
        }
    

    @staticmethod
    def from_dict(source):
        user_id = source.get('UserID', None)
        tickets = source.get('Tickets', [])
        return User(user_id, tickets)

    
    def save(self, db):
        doc_ref = db.collection('Users').document(self.user_id)
        doc_ref.set(self.to_dict())


    def add_ticket(self, db, ticket):
        from ticket import Ticket
        # Ensure that the ticket is in dictionary form before appending
        if isinstance(ticket, Ticket):
            ticket_dict = ticket.to_dict()
        else:
            ticket_dict = ticket  # assuming ticket is already a dict if not an instance of Ticket
        self.tickets.append(ticket_dict)
        self.save(db)


    def remove_ticket(self, db, ticket_id):
        ticket = self.get_ticket_by_id(ticket_id)
        if ticket:
            self.tickets.remove(ticket)
            self.save(db)
            return True
        print("Ticket", ticket_id, "is not in the user's tickets list")
        return False
    
    def get_ticket_by_id(self, ticket_id):
        for ticket in self.tickets:
            print(ticket)
            if ticket.get('TicketID') == ticket_id:  # Access 'TicketID' from the ticket dictionary
                return ticket
        return None
