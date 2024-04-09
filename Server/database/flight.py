class Flight:
    def __init__(self, flight_number, origin, destination, date, duration, price, status, seats):
        self.flight_number = flight_number
        self.origin = origin
        self.destination = destination
        self.date = date
        self.duration = duration
        self.price = price
        self.status = status
        self.seats = seats

    def to_dict(self):
        return {
            'FlightNumber': self.flight_number,
            'Origin': self.origin,
            'Destination': self.destination,
            'Date': self.date,
            'Duration': self.duration,
            'Price': self.price,
            'Status': self.status,
            'Seats': self.seats
        }
    
    def save(self, db):
        doc_ref = db.collection('Flights').document(self.flight_number)
        doc_ref.set(self.to_dict())