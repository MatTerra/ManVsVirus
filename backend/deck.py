from __future__ import annotations

from dataclasses import dataclass, field
from random import shuffle
from typing import Optional, List

from backend.card import Card


@dataclass
class Deck:
    cards: List = field(default_factory=list)
    drawn: List = field(default_factory=list)

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

    @classmethod
    def deserialize(cls, data: dict) -> Deck:
        deck = Deck()
        deck.drawn = [Card.deserialize(serialized_card) for serialized_card in
                      data.get('drawn')]
        deck.cards = [Card.deserialize(serialized_card) for serialized_card in
                      data.get('cards')]
        return deck
