from random import shuffle
from typing import Optional

from card import Card
import card


class Deck:
    def __init__(self):
        self.cards = list()
        self.drawn = list()

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
        return {'drawn': [card.serialize() for card in self.drawn],
                'cards': [card.serialize() for card in self.cards]}


def deserialize(data: dict) -> Deck:
    deck = Deck()
    deck.drawn = [card.deserialize(serialized_card) for serialized_card in data.get('drawn')]
    deck.cards = [card.deserialize(serialized_card) for serialized_card in data.get('cards')]
    return deck
