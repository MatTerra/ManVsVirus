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
        self.infections = [0]*4
        self.research_center = False

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
                'connections': {str(city.id): city.name for city in self.connections},}


CITIES = list()

for i in range(48):
    city = City(i, CITIES_DATA[i][0], CITIES_DATA[i][1], CITIES_DATA[i][2], CITIES_DATA[i][3])
    CITIES.append(city)

for i in range(48):
    for connection in CITIES_DATA[i][4]:
        CITIES[i].add_connection(CITIES[connection])
