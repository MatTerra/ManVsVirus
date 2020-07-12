from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, ClassVar

from backend.city import CITIES, City
from backend.constants import COLORS
from backend.board import Board
from backend.card import Card
from backend import card


@dataclass
class Player:
    ROLES: ClassVar[dict] = {1: "Doctor",
                             2: "Quarentine Expert",
                             3: "Travel Agent",
                             4: "Operations Expert",
                             5: "Scientist",
                             6: "Researcher",
                             7: "Contingency Expert"}
    id_: int
    role: int
    board: Board
    location: City = None
    cards: List[Card] = field(default_factory=list)

    def __post_init__(self):
        if self.location is None:
            self.location = self.board.locations[0]

    def possible_moves(self) -> List[City]:
        possible = list()
        possible += self.location.connections
        if self.location.research_center:
            possible += self.board.get_research_centers()
        if self.location in possible:
            possible.remove(self.location)
        possible = list(set(possible))
        possible.sort()
        return list(possible)

    def possible_travel_from(self) -> bool:
        return self.location in [_card.city for _card in self.cards if
                                 _card.city is not None]

    def possible_travel_to(self) -> List[City]:
        return [_card.city for _card in self.cards if _card.city is not None]

    def move(self, location: City):
        self.location = location

    def add_card(self, card: Card) -> int:
        self.cards.append(card)
        return len(self.cards)

    def serialize(self) -> dict:
        return {'id': self.id_,
                'role': Player.ROLES.get(self.role),
                'location': self.location.id_,
                'possible_moves': [{'name': city.name, 'id': city.id_} for city
                                   in self.possible_moves()],
                'cards': [card.serialize() for card in self.cards]}

    @classmethod
    def deserialize(cls, data: dict, board: Board) -> Player:
        player_id = data['id']
        player_role = {Player.ROLES[key]: key for key in Player.ROLES}[
            data['role']]
        player_location = board.locations[data['location']]
        player_cards = list()
        for serialized_card in data['cards']:
            deserialized_card = Card.deserialize(serialized_card)
            player_cards.append(deserialized_card)
        player = Player(id_=player_id, role=player_role, board=board,
                        location=player_location)
        player.cards = player_cards
        return player
