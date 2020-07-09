from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from backend.constants import CITIES_DATA, COLORS


def create_infections():
    return [0]*4


@dataclass
class City:
    id_: int = None
    name: str = None
    country: str = None
    population: float = field(default=None, compare=False)
    color: int = None
    connections: List[City] = field(default_factory=list,
                                    init=False, compare=False)
    locked_infection: bool = field(default=False, init=False, compare=False)
    infections: List[int] = field(default_factory=create_infections,
                                        init=False, compare=False)
    research_center: bool = field(default=False, init=False, compare=False)

    def infect(self, amount: int = 1, color: int = None) -> int:
        if amount > 3:
            raise ValueError("Infection is limited to 3!")
        if color is None:
            color = self.color
        outbreak = 0
        if not self.locked_infection:
            if self.infections[color]+amount > 3:
                print("outbreak in " + self.name)
                outbreak += 1
                self.infections[color] = 3
                self.lock_infection()
                for connected_city in self.connections:
                    outbreak += connected_city.infect(color=color)
            else:
                self.infections[color] += amount
        return outbreak

    def heal(self, all_infections: bool = False, color: int = None) -> None:
        if color is None:
            color = self.color
        if all_infections:
            self.infections[color] = 0
        else:
            self.infections[color] -= 1
        return None

    def lock_infection(self) -> None:
        self.locked_infection = True

    def unlock_infection(self) -> None:
        self.locked_infection = False

    def add_connection(self, city: object):
        self.connections.append(city)

    def serialize(self):
        return {'id': self.id_,
                'name': self.name,
                'country': self.country,
                'color': self.color,
                'connections': {str(connected_city.id_): connected_city.name
                                for connected_city in self.connections},
                'population': self.population,
                'infections': self.infections}

    @classmethod
    def deserialize(cls, data: dict) -> City:
        if data is None:
            return None
        if not {'id', 'name', 'color',
                'country', 'population'}.issubset(data.keys()):
            raise AssertionError("'id', 'name', 'color',"
                                 " 'country' and 'population' are required!")
        deserialized_city = City(id_=data.get('id'),
                                 color=data.get('color'),
                                 name=data.get('name'),
                                 population=data.get('population'),
                                 country=data.get('country'))
        deserialized_city.infections = (data.get('infections')
                                        if data.get('infections') is not None
                                        else [0]*4)
        return deserialized_city


CITIES = list()

for i in range(48):
    city = City(i, CITIES_DATA[i][0],
                CITIES_DATA[i][1],
                CITIES_DATA[i][2],
                CITIES_DATA[i][3])
    CITIES.append(city)

for i in range(48):
    for connection in CITIES_DATA[i][4]:
        CITIES[i].add_connection(CITIES[connection])
