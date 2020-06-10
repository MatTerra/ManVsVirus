import pytest
from backend.card import Card
from backend.city import City
from backend import card


class TestCard:
    @pytest.fixture
    def city(self) -> City:
        return City(0, "Atlanta", "USA", 10.0, 0)

    @pytest.fixture
    def city_card(self, city) -> Card:
        return Card(id=0, city=city)

    @pytest.fixture
    def action_card(self) -> Card:
        return Card(id=1, action="Epidemic")

    @pytest.mark.parametrize("card_1, card_2, result", [
                              (Card(id=0, city=City(0, "Atlanta", "USA", 10.0, 0)),
                               Card(id=0, city=City(0, "Atlanta", "USA", 10.0, 0)),
                               True),
                              (Card(id=0, city=City(0, "Atlanta", "USA", 10.0, 0)),
                               Card(id=1, city=City(1, "Chicago", "USA", 11.0, 0)),
                               False),
                              (Card(id=0, action='Epidemic'),
                               Card(id=0, city=City(0, "Atlanta", "USA", 10.0, 0)),
                               False),
                              (Card(id=0, action='Epidemic'),
                               Card(id=0, action='Epidemic'),
                               True),
                              (Card(id=0, action='Epidemic'),
                               Card(id=2, action='Travel'),
                               False)
    ])
    def test_eq(self, card_1: Card, card_2: Card, result: bool):
        assert (card_1 == card_2) == result

    @pytest.mark.parametrize("check_card, serialized", [
        (Card(id=0, city=City(0, "Atlanta", "USA", 10.0, 0)), {'id': 0,
                                                               'city': {'id': 0, 'name': 'Atlanta', 'country': 'USA',
                                                                        'color': 0, 'connections': {},
                                                                        'population': 10.0, 'infections': [0, 0, 0, 0]},
                                                               'type': 'city'}),
        (Card(id=0, action='Epidemic'), {'id': 0, 'action': 'Epidemic', 'type': 'action'})
    ])
    def test_serialization(self, check_card, serialized):
        assert check_card.serialize() == serialized

    @pytest.mark.parametrize("check_card",
                             [Card(id=0, action='Epidemic'), Card(id=0, city=City(0, "Atlanta", "USA", 10.0, 0))])
    def test_deserialization(self, check_card: Card):
        card_serialized = check_card.serialize()
        card_deserialized = card.deserialize(card_serialized)
        assert card_deserialized == check_card
