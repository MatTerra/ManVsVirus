from random import shuffle
from typing import Optional

from backend.card import Card
from backend import card


class Deck:
    def __init__(self):
        self.cards = list()
        self.drawn = list()

    def __eq__(self, other):
        if type(other) != type(self):
            return False
        return self.cards == other.cards and self.drawn == other.drawn

    def shuffle(self):
        shuffle(self.cards)

    def draw_card(self) -> Optional[Card]:
        try:
            drawn_card = self.cards.pop()
            self.drawn.append(drawn_card)
            return drawn_card
        except IndexError:
            return None

    def serialize(self):
        return {'drawn': [_card.serialize() for _card in self.drawn],
                'cards': [_card.serialize() for _card in self.cards]}


def deserialize(data: dict) -> Deck:
    deck = Deck()
    deck.drawn = [card.deserialize(serialized_card) for serialized_card in data.get('drawn')]
    deck.cards = [card.deserialize(serialized_card) for serialized_card in data.get('cards')]
    return deck
