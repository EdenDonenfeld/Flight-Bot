import uuid

class Ticket:
    def __init__(self, flight_number, seats, ticket_id=None):
        if ticket_id is None:
            self.ticket_id = self.generate_ticket_id()
        else:
            self.ticket_id = ticket_id
        self.flight_number = flight_number
        self.seats = seats

    def to_dict(self):
        return {
            'TicketID': self.ticket_id,
            'FlightNumber': self.flight_number,
            'Seats': self.seats
        }
    
    @staticmethod
    def from_dict(source):
        ticket_id = source.get('TicketID', None)
        flight_number = source.get('FlightNumber', None)
        seats = source.get('Seats', [])
        return Ticket(flight_number, seats, ticket_id)
    
    def save(self, db):
        doc_ref = db.collection('Tickets').document(self.ticket_id)
        doc_ref.set(self.to_dict())


    @staticmethod
    def generate_ticket_id():
        # 8 character ticket id
        return str(uuid.uuid4().hex[:8])
    

    def get_flight_num(self):
        return self.flight_number
    
    def get_ticket_id(self):
        return self.ticket_id