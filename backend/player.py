from typing import List

from backend.city import CITIES, City
from backend.constants import COLORS
from backend.board import Board
from backend.card import Card


class Player:
    ROLES = {1: "Doctor",
             2: "Quarentine Expert",
             3: "Travel Agent",
             4: "Operations Expert",
             5: "Scientist",
             6: "Researcher",
             7: "Contingency Expert"}

    def __init__(self, id: int, role: int, board: Board, location: City = CITIES[0]):
        self.id = id
        self.role = role
        self.board = board
        self.location = location
        self.cards = list()

    def possible_moves(self) -> List[City]:
        possible = list()
        possible += self.location.connections
        if self.location.research_center:
            possible += self.board.get_research_centers()
        if self.location in possible:
            possible.remove(self.location)
        return possible

    def possible_travel_from(self) -> bool:
        return self.location in [card.city for card in self.cards if card.city is not None]

    def possible_travel_to(self) -> List[City]:
        return [card.city for card in self.cards if card.city is not None]

    def move(self, location: City):
        if location in self.possible_moves():
            self.location = location
        else:
            raise Exception()

    def add_card(self, card: Card) -> int:
        self.cards.append(card)
        return len(self.cards)

    def serialize(self) -> dict:
        return {'id': self.id,
                'role': Player.ROLES.get(self.role),
                'location': {str(self.location.id): self.location.name},
                'possible_moves': {str(city.id): city.name for city in self.possible_moves()},
                'cards': {str(card.id): ({'type': 'city', 'name': card.city.name, 'color': COLORS[card.city.color], 'population': card.city.population}
                                    if card.city is not None
                                    else {'type': 'action', 'name': card.action}
                                    ) for card in self.cards}}
