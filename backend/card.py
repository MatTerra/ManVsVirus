from city import City
import city


class Card:
    def __init__(self, id: int = None, city: City = City(), action: str = None):
        self.id = id
        self.city = city
        self.action = action

    def serialize(self):
        if self.city is None:
            return {'id': self.id,
                    'action': self.action,
                    'type': 'action'}
        else:
            return {'id': self.id,
                    'city': self.city.serialize(),
                    'type': 'city'}


def deserialize(data: dict) -> Card:
    card = Card(id=data.get('id'), city=city.deserialize(data.get('city')), action=data.get('action'))
    return card