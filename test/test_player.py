# from pytest import fixture
from collections import Counter

import pytest
from backend.board import Board
from backend.card import Card
from backend.constants import CITIES_DATA
from backend.player import Player


class TestPlayer:
    @pytest.fixture
    def board(self):
        board = Board()
        board.initialize_board(cities=CITIES_DATA)
        return board

    @pytest.fixture
    def player(self, board):
        player = Player(id_=1, role=1, board=board)
        return player

    @pytest.fixture
    def serialized(self):
        return {'id': 1, 'role': 'Doctor', 'location': 0,
                'possible_moves': [{'name': 'Chicago', 'id': 1},
                                   {'name': 'Washington', 'id': 4},
                                   {'name': 'Miami', 'id': 25}],
                'cards': [
                    {'id': 0, 'city': {'id': 0,
                                       'name': 'Atlanta',
                                       'country': 'Estados Unidos',
                                       'color': 0,
                                       'connections':
                                           {'1': 'Chicago',
                                            '4': 'Washington',
                                            '25': 'Miami'},
                                       'population': 4.715,
                                       'infections': [0, 0, 0, 0]},
                     'type': 'city'}]}

    def test_post_init(self, player, board):
        assert player.location == board.locations[0]

    def test_get_possible_moves(self, player, board):
        # moves = player.possible_moves()
        # moves.sort(key=id)
        # board.locations[0].connections.sort(key=id)
        assert player.possible_moves() == board.locations[0].connections

    def test_add_card(self, board, player):
        card = Card(id_=0, city=board.locations[0])
        player.add_card(card)
        assert player.cards == [card]

    def test_possible_travel_from(self, board, player):
        card = Card(id_=0, city=board.locations[0])
        player.add_card(card)
        assert player.possible_travel_from()

    def test_travel_to(self, board, player):
        card = Card(id_=36, city=board.locations[36])
        player.add_card(card)
        assert player.possible_travel_to() == [board.locations[36]]

    def test_move(self, board, player):
        player.move(board.locations[34])
        assert player.location == board.locations[34]

    def test_serialize(self, board, player, serialized):
        card = Card(id_=0, city=board.locations[0])
        player.add_card(card)
        assert player.serialize() == serialized

    def test_deserialize(self, board, player, serialized):
        card = Card(id_=0, city=board.locations[0])
        player.add_card(card)
        assert Player.deserialize(data=serialized, board=board) == player
