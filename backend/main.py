import json

from backend.player import Player
from backend.board import Board
from backend.infection_deck import InfectionDeck
from backend.player_deck import PlayerDeck
from backend.constants import COLORS, FIREBASE
from backend.city import CITIES
from random import shuffle, choice
import string
import hashlib

from flask import abort

from firebase_admin import firestore


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

        infections = [location.infections for location in self.board.locations]
        infections_zip = list(zip(*infections))
        self.infection_sum = list(map(sum, infections_zip))

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

        infections = [location.infections for location in self.locations]
        infections_zip = list(zip(*infections))
        self.infection_sum = list(map(sum, infections_zip))
        if max(self.infection_sum > 24):
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
        serial = self.board.serialize()
        serial.update({
            'players': {str(player.id): player.serialize() for player in self.players},
            'outbreaks': self.outbreaks,
            'cures': {COLORS[i]: self.cures[i] for i in range(4)},
            'turn': {'player': self.turn_of, 'remaining_actions': self.remaining_actions},
            'infections_sum': self.infection_sum,
            'infection_deck': self.infection_deck.serialize(),
            'player_deck': self.player_deck.serialize()})
        return serial


def read_game(token_info: dict):
    try:
        user_id = token_info.get('primarysid')
    except:
        return abort(404, "Missing parameters")

    db = firestore.client()
    doc_ref_2 = db.collection('users_games').document(user_id).get()
    if not doc_ref_2.exists:
        abort(400, "User not in a game")
    game_id = doc_ref_2.to_dict().get('game')
    if game_id is None:
        abort(400, "User not in a game")

    doc_ref = db.collection('games').document(game_id).get()
    if not doc_ref.exists:
        abort(404, "Game doesn't exists")
    game_dict = doc_ref.to_dict()
    game_dict.pop('password')
    game_dict.pop('infection_deck')
    game_dict.pop('player_deck')
    return game_dict


def create_game(game_data: dict, token_info: dict):
    try:
        user_id = token_info.get('primarysid')
        num_players = game_data['num_players']
        difficulty = game_data['difficulty']
        password = game_data['password'].encode('utf-8')
    except:
        return abort(404, "Missing parameters")

    game = Controller(num_players, difficulty)
    # Use a service account

    db = firestore.client()
    doc_ref_2 = db.collection('users_games').document(user_id).get()
    if doc_ref_2.exists:
        abort(400, "User already in a game")

    lettersAndDigits = string.ascii_letters + string.digits
    game_id = ''.join((choice(lettersAndDigits) for i in range(32)))

    doc_ref = db.collection('games').document(game_id)
    game_serialized = game.serialize()
    users = {str(i): None for i in range(1, num_players)}
    users['0'] = user_id
    game_serialized.update({'users': users,
                            'password': str(hashlib.sha256(password).hexdigest())})
    doc_ref.set(game_serialized)

    doc_ref_2 = db.collection('users_games').document(user_id)
    doc_ref_2.set({'game': game_id})

    return game_id



def join_game(game_id: str, data: dict, token_info: dict):
    try:
        user_id = token_info.get('primarysid')
        password = data['password'].encode('utf-8')
    except:
        return abort(404, "Missing parameters")

    db = firestore.client()
    doc_ref_2 = db.collection('users_games').document(user_id).get()
    if doc_ref_2.exists:
        abort(400, "User already in a game")

    doc_ref = db.collection('games').document(game_id).get()
    if not doc_ref.exists:
        abort(404, "Game doesn't exists")
    game_dict = doc_ref.to_dict()
    if game_dict.get('password') != str(hashlib.sha256(password).hexdigest()):
        abort(401, "Wrong Password")

    users = game_dict.get('users')

    for key in users.keys():
        if users[key] is None:
            doc_ref = db.collection('games').document(game_id)
            users[key] = user_id
            doc_ref.update({'users': users})
            break

    doc_ref_2 = db.collection('users_games').document(user_id)
    doc_ref_2.set({'game': game_id})


if __name__ == '__main__':
    num_players = int(input("Welcome! Number of players(2-4)? "))
    while num_players not in range(2, 5):
        num_players = int(input("Welcome! Number of players(2-4)? "))

    difficulty = int(input("How difficult will the game be(1-3)?"))
    while difficulty not in range(1, 4):
        difficulty = int(input("How difficult will the game be(1-3)?"))

    game = Controller(num_players, difficulty)
    print(game.serialize())

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
