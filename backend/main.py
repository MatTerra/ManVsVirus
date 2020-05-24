import json

from backend.player import Player
from backend.board import Board
from backend.infection_deck import InfectionDeck
from backend.player_deck import PlayerDeck
from backend.constants import COLORS
from backend.city import CITIES
from random import shuffle


class Controller:
    def __init__(self, num_players: int = 2, difficulty: int = 0):
        self.board = Board()

        self.cures = [False, False, False, False]

        self.lost = False

        self.infection_deck = InfectionDeck()
        self.infection_deck.shuffle()

        for i in range(3):
            for j in range(3):
                card = self.infection_deck.draw_card()
                self.board.locations[card.city.id].infect(amount=(3 - i))
                print(str(self.board.locations[card.city.id].infections))

        self.player_deck = PlayerDeck(difficulty + 2)
        self.player_deck.shuffle()

        self.outbreaks = 0

        roles = list(Player.ROLES.keys())

        shuffle(roles)
        self.players = list()
        for i in range(num_players):
            role = roles.pop()
            player = Player(i, role, self.board)
            for i in range(2):
                player.add_card(self.player_deck.draw_card())
            self.players.append(player)

        self.player_deck.add_epidemics()

        self.turn_of = 0
        self.remaining_actions = 4
        self.max_pop = 0
        for player in self.players:
            for card in player.cards:
                if card.city.population > self.max_pop:
                    self.turn_of = player.id
                    self.max_pop = card.city.population

    def play_action(self, action: dict):
        player = self.players[self.turn_of]
        if action.get('type') == 'move':
            self.move_player(action, player)
        elif action.get('type') == 'heal':
            player.location.heal(player.role == 1 or self.cures[player.location.color], action.get('data').get('color'))
        elif action.get('type') == 'skip':
            return self.end_round()
        self.remaining_actions -= 1
        if self.remaining_actions == 0:
            self.end_round()

    def end_round(self):
        if not self.player_card_stage(self.turn_of):
            self.lost = True
            self.turn_of = None

        self.infection_stage()
        if self.outbreaks > 7:
            self.lost = True
            self.turn_of = None

        if self.lost:
            return

        self.board.unlock_cities()

        self.turn_of += 1
        if self.turn_of == len(self.players):
            self.turn_of = 0
        self.remaining_actions = 4

    def player_card_stage(self, player_id: int) -> bool:
        for i in range(2):
            drawn_card = self.player_deck.draw_card()
            if drawn_card is None:
                return False
            if drawn_card.action == "Epidemic":
                print("Epidemic")
                self.epidemic()
            else:
                self.players[player_id].add_card(drawn_card)
        return True

    def epidemic(self):
        # Speed up
        self.board.current_speed += 1

        # Infect
        card = self.infection_deck.draw_last()
        self.outbreaks += self.board.infect(card.city.id, 3)

        # Return drawn
        self.infection_deck.return_drawn()

    def infection_stage(self):
        cities = list()
        for i in range(self.board.infection_speeds[self.board.current_speed]):
            card = self.infection_deck.draw_card()
            if card is not None:
                self.outbreaks += self.board.infect(card.city.id)
                cities.append(self.board.locations[card.city.id])
            else:
                return cities
        return cities

    def move_player(self, action, player):
        destination = action.get('data')
        destination_id = destination.get('destination')
        if CITIES[destination_id] not in player.possible_moves():
            raise ValueError("City not available to move")
        player.move(CITIES[action.get('data').get('destination')])

    def serialize(self):
        return {'board': self.board.serialize(),
                'players': [player.serialize() for player in self.players],
                'outbreaks': self.outbreaks,
                'cures': {COLORS[i]: self.cures[i] for i in range(4)},
                'turn': {'player': self.turn_of, 'remaining_actions': self.remaining_actions}}


if __name__ == '__main__':
    num_players = int(input("Welcome! Number of players(2-4)? "))
    while num_players not in range(2, 5):
        num_players = int(input("Welcome! Number of players(2-4)? "))

    difficulty = int(input("How difficult will the game be(1-3)?"))
    while difficulty not in range(1, 4):
        difficulty = int(input("How difficult will the game be(1-3)?"))

    game = Controller(num_players, difficulty)
    game.board.infect(0, 2)
    game.cures[0] = True
    print(json.dumps(game.serialize()))
    game.play_action({"type": "heal", 'data': dict()})
    print(json.dumps(game.serialize()))
    for i in range(10):
        if game.players[game.turn_of].role == 1:
            game.play_action({"type": "heal", 'data': dict()})
            print("Doctor healed")
        game.play_action({"type": "skip"})
        if game.lost == True:
            print("lost")
            break
        # game.play_action(
        #     {'type': 'move', 'data': {'destination': game.players[game.turn_of].possible_moves()[i % 2].id}})
        print("round " + str(i))

    print(json.dumps(game.serialize()))
