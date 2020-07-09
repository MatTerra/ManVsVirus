from pytest import fixture, mark, raises
from pytest_assume.plugin import assume

from backend.city import City, create_infections
import backend.city


class TestCity:

    @fixture
    def city(self) -> City:
        return City(0, "Atlanta", "USA", 10.0, 0)

    def test_create_infections(self):
        assert create_infections() == [0, 0, 0, 0]

    def test_serialize(self, city):
        city_serialized = city.serialize()
        serialized = {'id': 0, 'name': 'Atlanta', 'country': 'USA',
                      'color': 0, 'connections': {}, 'population': 10.0,
                      'infections': [0, 0, 0, 0]}
        assert serialized == city_serialized

    def test_deserialize(self, city):
        city_deserialized = City.deserialize(city.serialize())
        assert city.__dict__ == city_deserialized.__dict__

    @mark.parametrize("other, result", [
        (City(0, "Atlanta", "USA", 10.0, 0), True),
        (City(0, "Atlanta", "USA", 11.0, 0), True),
        (City(0, "Chicago", "USA", 11.0, 0), False)])
    def test_eq(self, city, other, result):
        assume((city == other) == result)
        city.infect(1)
        city.connections.append(other)
        assume((city == other) == result)

    def test_infect_over_limit(self, city):
        with raises(ValueError):
            city.infect(amount=4)

    def test_infect_multiple_outbreak(self, city):
        city.infect(amount=1)
        outbreaks = city.infect(amount=3)
        assert city.infections[city.color] == 3 and outbreaks == 1

    @mark.parametrize("amount", [1, 2])
    @mark.parametrize("color", [None, 2])
    def test_infect(self, color, city, amount):
        city.infect(color=color, amount=amount)
        assert city.infections == [0
                                   if i != (city.color
                                            if color is None
                                            else color)
                                   else amount for i in range(4)]

    @mark.parametrize("all_infections", [True, False])
    @mark.parametrize("color", [None, 2])
    def test_heal(self, city, all_infections, color):
        city.infect(amount=2, color=color)
        city.heal(all_infections=all_infections, color=color)
        assert city.infections == [0
                                   if i != (city.color
                                            if color is None
                                            else color) or all_infections
                                   else 1
                                   for i in range(4)]

    def test_unable_to_deserialize(self):
        with raises(AssertionError):
            City.deserialize({'id': 0,
                              'key1': 0,
                              'key2': 1,
                              'key3': 2,
                              'key4': 3,
                              'key5': 4})

    def test_lock_unlock_infection(self, city):
        city.lock_infection()
        assume(city.locked_infection)

        city.infect(amount=1)
        assume(city.infections == [0] * 4)

        city.unlock_infection()
        assume(not city.locked_infection)

        city.infect(amount=1)
        assume(city.infections == [0
                                   if i != city.color
                                   else 1
                                   for i in range(4)])
