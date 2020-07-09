from pytest import fixture

from backend.city import CITIES
from backend.infection_deck import InfectionDeck


class TestInfectionDeck:
    @fixture
    def infection_deck(self):
        infection_deck = InfectionDeck()
        infection_deck.init_infection()
        return infection_deck

    def test_init_infection(self, infection_deck):
        assert [card.city for card in infection_deck.cards] == CITIES

    def test_return_drawn(self, infection_deck):
        cards = infection_deck.cards.copy()
        infection_deck.draw_card()
        infection_deck.return_drawn()
        assert cards == infection_deck.cards

    def test_draw_last(self, infection_deck):
        last = infection_deck.cards[0]
        drawn = infection_deck.draw_last()
        assert drawn == last
