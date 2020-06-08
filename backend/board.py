from city import City
from constants import CITIES_DATA
import city


class Board:
    def __init__(self):
        self.locations = list()
        self.research_centers = list()
        self.current_speed = 0
        self.infection_speeds = (2, 2, 2, 3, 3, 4, 4)

    def initialize_board(self, cities: list = CITIES_DATA):
        for i in range(48):
            city = City(i, cities[i][0], cities[i][1], cities[i][2], cities[i][3])
            self.locations.append(city)

        for i in range(48):
            for connection in cities[i][4]:
                self.locations[i].add_connection(self.locations[connection])

        self.research_centers = list()
        self.current_speed = 0
        self.infection_speeds = (2, 2, 2, 3, 3, 4, 4)
        self.add_research_center(0)

    def infect(self, location: int, amount: int = 1):
        outbreaks = self.locations[location].infect(amount)

        return outbreaks

    def add_research_center(self, city_id: int):
        self.locations[city_id].research_center = True
        if len(self.research_centers) == 6:
            self.research_centers.pop(0).research_center = False
        self.research_centers.append(self.locations[city_id])

    def get_research_centers(self):
        return self.research_centers

    def unlock_cities(self):
        for city in self.locations:
            city.unlock_infection()

    def serialize(self):
        return {'cities': {str(city.id): city.serialize() for city in self.locations},
                'research_centers': [city.id for city in self.research_centers],
                'infection_speed': self.infection_speeds[self.current_speed],
                'current_speed': self.current_speed,
                'infections': {str(location.id): location.infections for location in self.locations}}


def deserialize(data: dict):
    deserialized_board = Board()
    data['cities'] = {int(key): data.get('cities')[key] for key in data.get('cities')}
    print(sorted(data.get('cities')))

    for serialized_city in sorted(data.get('cities')):
        deserialized_board.locations.append(city.deserialize(data.get('cities')[serialized_city]))
    for serialized_city in sorted(data.get('cities')):
        for connection in data.get('cities')[serialized_city].get('connections'):
            deserialized_board.locations[int(serialized_city)].add_connection(deserialized_board.locations[int(connection)])
    for research_center in data.get('research_centers'):
        deserialized_board.add_research_center(research_center)
    deserialized_board.current_speed = data.get('current_speed')
    for infections in data.get('infections'):
        deserialized_board.locations[int(infections)].infections = data.get('infections')[infections]
    return deserialized_board


if __name__ == '__main__':
    board = Board()
    board.start_game().keys()
    board.infection_deck.return_drawn()
    cidades = board.infection_stage()
    for cidade in cidades:
        print(cidade.serialize())
        print(board.outbreaks)

    print(board.locations[0].serialize())
    for i in range(6):
        board.add_research_center(board.locations[i + 1])
        print(board.research_centers)

    print(board.locations[0].serialize())
    print(board.serialize())
