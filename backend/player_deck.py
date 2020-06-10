from random import shuffle

from backend.city import CITIES
from backend.card import Card
from backend.deck import Deck


class PlayerDeck(Deck):
    def __init__(self, difficulty: int = 3):
        super().__init__()
        self.difficulty = difficulty

    def init_player_deck(self):
        self.card_id = 0
        for city in CITIES:
            card = Card(self.card_id, city)
            self.cards.append(card)
            self.card_id += 1

    def add_epidemics(self):
        decks_quant = int(len(self.cards) / self.difficulty)
        decks = [self.cards[x * decks_quant:(decks_quant * x) + decks_quant if x < self.difficulty - 1 else None]
                 for x in range(self.difficulty)]
        for i in range(self.difficulty):
            card = Card(self.card_id, action='Epidemic')
            self.card_id += 1
            decks[i].append(card)
            shuffle(decks[i])
        self.cards = list()
        for deck_with_epidemic in decks:
            self.cards += deck_with_epidemic


if __name__ == '__main__':
    deck = PlayerDeck()
    deck.shuffle()
    print(str([card.city.name if card.city is not None else card.action for card in deck.deck]))
    deck.add_epidemics()
    print(str([card.city.name if card.city is not None else card.action for card in deck.deck]))
