from backend.city import City


class Card:
    def __init__(self, id: int = None, city: City = None, action: str = None):
        self.id = id
        self.city = city
        self.action = action

    def serialize(self):
        if self.city is None:
            return {'id': self.id,
                    'action': self.action}
        else:
            return {'id': self.id,
                    'city': self.city.serialize()}
