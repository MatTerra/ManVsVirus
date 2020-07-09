from __future__ import annotations

from dataclasses import dataclass

from backend.city import City
from backend import city

@dataclass
class Card:
    id_: int = None
    city: City = None
    action: str = None

    def serialize(self):
        if self.city is None:
            return {'id': self.id_,
                    'action': self.action,
                    'type': 'action'}
        else:
            return {'id': self.id_,
                    'city': self.city.serialize(),
                    'type': 'city'}

    @classmethod
    def deserialize(cls, data: dict) -> Card:
        if type(data) != dict:
            raise TypeError("data must be a dict!")
        if data.get('id') is None:
            raise AssertionError("Card must have an id!")
        if data.get('city') is None and data.get('action') is None:
            raise AssertionError("Card must have an action or a city!")

        card = Card(id_=data.get('id'),
                    city=City.deserialize(data.get('city')),
                    action=data.get('action'))
        return card
