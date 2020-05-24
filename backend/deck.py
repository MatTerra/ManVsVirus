from random import shuffle
from typing import Optional

from backend.card import Card


class Deck:
    def __init__(self):
        self.deck = list()
        self.drawn = list()

    def shuffle(self):
        shuffle(self.deck)

    def draw_card(self) -> Optional[Card]:
        try:
            drawn_card = self.deck.pop()
            self.drawn.append(drawn_card)
            return drawn_card
        except IndexError:
            return None
