import pytest
from backend.city import City
import backend.city


class TestCity:
    @pytest.fixture
    def city(self):
        return City(0, "Atlanta", "USA", 10.0, 0)

    def test_serialize(self, city):
        city_serialized = city.serialize()
        serialized = {'id': 0, 'name': 'Atlanta', 'country': 'USA', 'color': 0, 'connections': {}, 'population': 10.0,
                      'infections': [0, 0, 0, 0]}
        assert serialized == city_serialized

    def test_deserialize(self, city):
        city_deserialized = backend.city.deserialize(city.serialize())
        assert city.__dict__ == city_deserialized.__dict__

    @pytest.mark.parametrize("other, result", [
        (City(0, "Atlanta", "USA", 10.0, 0), True),
        (City(0, "Atlanta", "USA", 11.0, 0), True),
        (City(0, "Chicago", "USA", 11.0, 0), False)])
    def test_eq(self, city, other, result):
        pytest.assume((city == other) == result)
        city.infect(1)
        city.connections.append(other)
        pytest.assume((city == other) == result)

    @pytest.mark.parametrize("amount", [1, 2])
    @pytest.mark.parametrize("color", [None, 2])
    def test_infect(self, color, city, amount):
        city.infect(color=color, amount=amount)
        assert city.infections == [0 if i != (city.color if color is None else color) else amount for i in range(4)]
        city.infections = [0]*4

    @pytest.mark.parametrize("all", [True, False])
    @pytest.mark.parametrize("color", [None, 2])
    def test_heal(self, city, all, color):
        city.infect(amount=2, color=color)
        city.heal(all=all, color=color)
        assert city.infections == [0 if i != (city.color if color is None else color) or all else 1 for i in range(4)]
        city.infections = [0]*4

    def test_lock_unlock_infection(self, city):
        city.lock_infection()
        pytest.assume(city.locked_infection == True)

        city.infect(amount=1)
        pytest.assume(city.infections == [0]*4)

        city.unlock_infection()
        pytest.assume(city.locked_infection == False)

        city.infect(amount=1)
        pytest.assume(city.infections == [0 if i != city.color else 1 for i in range(4)])

        city.infections = [0] * 4

