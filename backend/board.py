from backend.city import CITIES, City


class Board:
    def __init__(self):
        self.locations = CITIES
        self.research_centers = list()
        self.current_speed = 0
        self.infection_speeds = (2,2,2,3,3,4,4)
        self.add_research_center(CITIES[0])

    def infect(self, location: int, amount: int = 1):
        outbreaks = self.locations[location].infect(amount)
        return outbreaks

    def add_research_center(self, city: City):
        city.research_center = True;
        if len(self.research_centers) < 6:
            self.research_centers.append(city)
        else:
            self.research_centers.pop(0).research_center = False
            self.research_centers.append(city)

    def get_research_centers(self):
        return self.research_centers

    def unlock_cities(self):
        for city in self.locations:
            city.unlock_infection()

    def serialize(self):
        return {'cities': {str(city.id): city.serialize() for city in self.locations}}#,
        #         u'research_centers': {str(city.id).encode('utf-8'): city.name.encode('utf-8') for city in self.research_centers},
        #         u'infection_speed': str(self.infection_speeds[self.current_speed]).encode('utf-8')}
        return dict()

if __name__ == '__main__':
    board = Board()
    board.start_game()
    board.infection_deck.return_drawn()
    cidades = board.infection_stage()
    for cidade in cidades:
        print(cidade.serialize())
        print(board.outbreaks)

    print(CITIES[0].serialize())
    for i in range(6):
        board.add_research_center(CITIES[i+1])
        print(board.research_centers)

    print(CITIES[0].serialize())
    print(board.serialize())
