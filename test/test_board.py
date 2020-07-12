from pytest import fixture
from pytest_assume.plugin import assume

from backend.board import Board
from backend.city import City
from backend.constants import CITIES_DATA


class TestBoard:
    @fixture
    def serialized(self):
        return {'cities':
                    {'0': {'id': 0,
                           'name': 'Atlanta',
                           'country': 'Estados Unidos',
                           'color': 0,
                           'connections': {'1': 'Chicago'},
                           'population': 4.715,
                           'infections': [3, 0, 0, 0]
                           },
                     '1': {'id': 1,
                           'name': 'Chicago',
                           'country': 'Estados Unidos',
                           'color': 0,
                           'connections': {'0': 'Atlanta'},
                           'population': 9.121,
                           'infections': [1, 0, 0, 0]
                           }
                     },
                'research_centers': [0],
                'infection_speed': 2,
                'current_speed': 0,
                'infections': {'0': [3, 0, 0, 0],
                               '1': [1, 0, 0, 0]}}

    @fixture
    def board(self) -> Board:
        board = Board()
        board.initialize_board(cities=CITIES_DATA[:10])
        return board

    def test_init(self):
        board = Board()
        assume(board.locations == [])
        assume(board.research_centers == [])
        assume(board.current_speed == 0)
        assume(board.infection_speeds == [2, 2, 2, 3, 3, 4, 4])

    def test_initialize_board(self, board):
        assume(board.research_centers == [board.locations[0]])
        assume(len(board.locations) == 10)
        assume(len(board.locations[0].connections) > 0)

    def test_infect(self, board):
        board.infect(location=0, amount=2)
        assert board.locations[0].infections == [2, 0, 0, 0]

    def test_add_research_center(self, board):
        board.add_research_center(1)
        assert board.get_research_centers() == board.locations[:2]

    def test_add_over_limit_research_center(self, board):
        for i in range(1, 7):
            board.add_research_center(i)
        assert board.get_research_centers() == board.locations[1:7]

    def test_unlock_cities(self, board):
        for city in board.locations:
            city.lock_infection()
        board.unlock_cities()
        assume(
            list(filter(lambda city: city.locked_infection,
                        board.locations)) == []
        )

    def test_serialize(self, serialized):
        board = Board()
        board.initialize_board(cities=CITIES_DATA[:2])
        board.infect(0, 2)
        board.infect(0, 2)
        assert board.serialize() == serialized

    def test_deserialize(self, serialized):
        board = Board()
        board.initialize_board(cities=CITIES_DATA[:2])
        board.infect(0, 2)
        board.infect(0, 2)
        assert Board.deserialize(serialized) == board
