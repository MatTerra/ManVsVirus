from backend.constants import CITIES_DATA, COLORS


class City:
    def __init__(self, id: int = None, name: str = None, country: str = None, population: float = None,
                 color: int = None):
        self.id = id
        self.color = color
        self.name = name
        self.population = population
        self.connections = list()
        self.country = country
        self.locked_infection = False
        self.infections = [0] * 4
        self.research_center = False

    def __eq__(self, other):
        if type(other) != City:
            return False
        self_dict = self.__dict__.copy()
        self_dict.pop('connections')
        self_dict.pop('infections')
        self_dict.pop('population')
        other_dict = other.__dict__.copy()
        other_dict.pop('connections')
        other_dict.pop('infections')
        other_dict.pop('population')
        return self_dict == other_dict

    def infect(self, amount: int = 1, color: int = None) -> int:
        if color is None:
            color = self.color
        outbreak = 0
        if not self.locked_infection:
            if self.infections[color] == 3:
                print("outbreak in " + self.name)
                outbreak += 1
                self.lock_infection()
                for city in self.connections:
                    outbreak += city.infect(color=color)
            else:
                self.infections[color] += amount
        return outbreak

    def heal(self, all: bool = False, color: int = None) -> None:
        if color is None:
            color = self.color
        if all:
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
        return {'id': self.id,
                'name': self.name,
                'country': self.country,
                'color': self.color,
                'connections': {str(city.id): city.name for city in self.connections},
                'population': self.population,
                'infections': self.infections}


def deserialize(data: dict) -> City:
    if data is None:
        return None
    deserialized_city = City()
    deserialized_city.id = data.get('id')
    deserialized_city.color = data.get('color')
    deserialized_city.name = data.get('name')
    deserialized_city.population = data.get('population')
    deserialized_city.country = data.get('country')
    deserialized_city.infections = data.get('infections') if data.get('infections') is not None else [0]*4
    return deserialized_city


CITIES = list()

for i in range(48):
    city = City(i, CITIES_DATA[i][0], CITIES_DATA[i][1], CITIES_DATA[i][2], CITIES_DATA[i][3])
    CITIES.append(city)

for i in range(48):
    for connection in CITIES_DATA[i][4]:
        CITIES[i].add_connection(CITIES[connection])
