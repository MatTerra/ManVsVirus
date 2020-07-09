from dataclasses import dataclass
from random import shuffle
from typing import Optional

from backend.deck import Deck
from backend.card import Card
from backend.city import CITIES


@dataclass
class InfectionDeck(Deck):

    def init_infection(self):
        card_id = 0
        for city in CITIES:
            card_ = Card(id_=card_id, city=city)
            self.cards.append(card_)
            card_id += 1

    def return_drawn(self) -> None:
        shuffle(self.drawn)
        self.cards += self.drawn
        self.drawn = list()
        return None

    def draw_last(self) -> Optional[Card]:
        self.cards.reverse()
        card_ = self.draw_card()
        self.cards.reverse()
        return card_
