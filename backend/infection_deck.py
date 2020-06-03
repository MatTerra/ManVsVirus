from random import shuffle
from typing import Optional

from backend.deck import Deck
from backend.card import Card
from backend.city import CITIES


class InfectionDeck(Deck):

    def __init__(self):
        super().__init__()
        card_id = 0
        for city in CITIES:
            card = Card(card_id, city)
            self.deck.append(card)
            card_id += 1

    def return_drawn(self) -> None:
        shuffle(self.drawn)
        self.deck += self.drawn
        self.drawn = list()
        return None

    def draw_last(self) -> Optional[Card]:
        self.deck.reverse()
        card = self.draw_card()
        self.deck.reverse()
        return card


if __name__ == '__main__':
    deck = InfectionDeck()
    deck.shuffle()
    deck.shuffle()
    card = deck.draw_card()
    print(card.city.name + "\t" + str(card.city.color))
    card = deck.draw_card()
    print(card.city.name + "\t" + str(card.city.color))
    deck.return_drawn()
    card = deck.draw_card()
    while card is not None:
        print(card.city.name + "\t" + str(card.city.color))
        card = deck.draw_card()
