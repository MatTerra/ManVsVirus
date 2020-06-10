import pytest
from backend.card import Card
from backend.city import City
from backend.deck import Deck
from backend.city import CITIES
from backend import card
from backend import deck


class TestDeck:    
    @pytest.fixture
    def reduced_deck(self) -> Deck:
        cards = list()
        for city in CITIES[:10]:
            new_card = Card(id=city.id, city=city)
            cards.append(new_card)
        reduced_deck = Deck()
        reduced_deck.cards = cards
        return reduced_deck

    def test_shuffle(self, reduced_deck: Deck):
        reduced_deck.shuffle()
        assert [_card.id for _card in reduced_deck.cards] != range(len(reduced_deck.cards))

    def test_draw(self, reduced_deck: Deck):
        for i in range(5):
            _card = reduced_deck.draw_card()
            pytest.assume(_card == reduced_deck.drawn[i])

    def test_draw_last(self, reduced_deck: Deck):
        for i in range(len(reduced_deck.cards)):
            _card = reduced_deck.draw_card()
        assert reduced_deck.draw_card() is None

    def test_serialization(self, reduced_deck: Deck):
        serialized_deck = reduced_deck.serialize()
        deserialized_deck: Deck = deck.deserialize(serialized_deck)
        assert reduced_deck == deserialized_deck
