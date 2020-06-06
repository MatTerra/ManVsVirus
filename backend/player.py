from typing import List

from city import CITIES, City
from constants import COLORS
from board import Board
from card import Card
import card


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
                'location': self.location.id,
                'possible_moves': [{'name': city.name, 'id': city.id} for city in self.possible_moves()],
                'cards': [card.serialize() for card in self.cards]}


def deserialize(data: dict, board: Board) -> Player:
    player_id = data['id']
    player_role = {Player.ROLES[key]: key for key in Player.ROLES}[data['role']]
    player_location = board.locations[data['location']]
    player_cards=list()
    for serialized_card in data['cards']:
        deserialized_card = card.deserialize(serialized_card)
        player_cards.append(deserialized_card)
    player = Player(id=player_id, role=player_role, board=board, location=player_location)
    player.cards = player_cards
    return player
