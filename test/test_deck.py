from pytest_assume.plugin import assume
from pytest import fixture

from backend.card import Card
from backend.deck import Deck
from backend.city import CITIES


class TestDeck:    
    @fixture
    def reduced_deck(self) -> Deck:
        cards = list()
        for city in CITIES[:10]:
            new_card = Card(id_=city.id_, city=city)
            cards.append(new_card)
        reduced_deck = Deck()
        reduced_deck.cards = cards
        return reduced_deck

    def test_shuffle(self, reduced_deck: Deck):
        ordered_deck_cards = reduced_deck.cards.copy()
        reduced_deck.shuffle()
        assert ordered_deck_cards != reduced_deck.cards

    def test_draw(self, reduced_deck: Deck):
        for i in range(5):
            _card = reduced_deck.draw_card()
            assume(_card == reduced_deck.drawn[i])

    def test_draw_empty(self):
        deck = Deck()
        assert deck.draw_card() is None

    def test_serialization(self, reduced_deck: Deck):
        serialized_deck = reduced_deck.serialize()
        deserialized_deck: Deck = Deck.deserialize(serialized_deck)
        assert reduced_deck == deserialized_deck
