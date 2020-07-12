from random import shuffle, choice
import string
import hashlib

from flask import abort

from firebase_admin import firestore

import json

from backend.player import Player
from backend import player
from backend.board import Board
from backend.infection_deck import InfectionDeck
from backend.player_deck import PlayerDeck
from backend import deck
from backend.constants import COLORS, FIREBASE
from backend import board


class Controller:
    def __init__(self, num_players: int = 2, difficulty: int = 0,
                 board: Board = None, cures: list = [False] * 4,
                 lost: bool = False, infection_deck: InfectionDeck = None,
                 infection_sum: list = [0] * 4, player_deck: PlayerDeck = None,
                 outbreaks: int = 0, players: list = [], turn_of: int = None,
                 remaining_actions: int = 4, discard: int = 0):
        self.board = board
        self.cures = cures
        self.lost = lost
        self.infection_deck = infection_deck
        self.infection_sum = infection_sum
        self.player_deck = player_deck
        self.outbreaks = outbreaks
        self.players = players
        self.turn_of = turn_of
        self.remaining_actions = remaining_actions
        self.difficulty = difficulty
        self.num_players = num_players
        self.discard = discard

    def start_game(self):
        self.board = Board()
        self.board.initialize_board()

        self.cures = [False] * 4

        self.lost = False

        self.infection_deck = InfectionDeck()
        self.infection_deck.init_infection()
        self.infection_deck.shuffle()

        for i in range(3):
            for j in range(3):
                card = self.infection_deck.draw_card()
                self.board.locations[card.city.id_].infect(amount=(3 - i))
                print(str(self.board.locations[card.city.id_].infections))

        infections = [location.infections for location in self.board.locations]
        infections_zip = list(zip(*infections))
        self.infection_sum = list(map(sum, infections_zip))

        self.player_deck = PlayerDeck(self.difficulty + 2)
        self.player_deck.init_player_deck()
        self.player_deck.shuffle()
        self.outbreaks = 0

        roles = list(Player.ROLES.keys())

        shuffle(roles)
        self.players = list()
        for j in range(self.num_players):
            role = roles.pop()
            player = Player(j, role, self.board)
            for j in range(2):
                player.add_card(self.player_deck.draw_card())
            self.players.append(player)

        self.player_deck.add_epidemics()

        self.turn_of = 0
        self.remaining_actions = 4
        max_pop = 0
        for player in self.players:
            for card in player.cards:
                if card.city.population > max_pop:
                    self.turn_of = player.id_
                    max_pop = card.city.population

    def play_action(self, action: dict):
        player = self.players[self.turn_of]
        if self.discard > 0 and action.get('type') != 'discard':
            raise ValueError("Can only discard now!")
        if action.get('type') == 'move':
            self.move_player(int(action['data']), player)
        elif action.get('type') == 'heal':
            player.location.heal(
                player.role == 1 or self.cures[int(action.get('data'))],
                int(action.get('data')) if action.get('data') != '' else None)
            infections = [location.infections for location in
                          self.board.locations]
            infections_zip = list(zip(*infections))
            self.infection_sum = list(map(sum, infections_zip))
        elif action.get('type') == 'travel':
            self.travel_player(int(action['data']), player)
        elif action.get('type') == 'skip':
            return self.end_round()
        elif action.get('type') == 'build':
            self.build(player)
        elif action.get('type') == 'cure':
            self.cure(int(action['data']), player)
        elif action.get('type') == 'discard':
            self.discard_action(int(action['data']), player)
            return self.end_round(action.get('type') == 'discard')

        self.remaining_actions -= 1
        if self.remaining_actions == 0:
            self.end_round()

    def build(self, player):
        if player.location.name not in [card.city.name for card in player.cards
                                        if card.city is not None] \
                and player.role != 4:
            raise ValueError("City card not available")
        if player.role != 4:
            action_cards = [card for card in player.cards if card.city is None]
            location_cards = [card for card in player.cards if
                              card.city is not None]
            player.cards = [card for card in location_cards if
                            card.city.id != player.location.id] + action_cards
        self.board.add_research_center(player.location.id)

    def cure(self, color, player):
        amount_to_cure = 5 if player.role != 5 else 4
        location_cards = [card for card in player.cards if
                          card.city is not None]
        action_cards = [card for card in player.cards if card.city is None]
        cards_to_cure = [card for card in location_cards if
                         card.city.color == color]
        if len(cards_to_cure) < amount_to_cure:
            raise ValueError("Not enough cards to cure")
        while len(cards_to_cure) > amount_to_cure:
            cards_to_cure.pop(0)
        location_cards = [card for card in location_cards if
                          card not in cards_to_cure]
        player.cards = location_cards + action_cards
        self.cures[color] = True

    def discard_action(self, card_id, player):
        player.cards = [card for card in player.cards if card.id != card_id]
        self.discard -= 1

    def end_round(self, skip_player: bool = False):
        if not skip_player:
            if not self.player_card_stage(self.turn_of):
                self.lost = True

        if len(self.players[self.turn_of].cards) > 7:
            self.discard = len(self.players[self.turn_of].cards) - 7
            return

        self.infection_stage()
        if self.outbreaks > 7:
            self.lost = True

        infections = [location.infections for location in self.board.locations]
        infections_zip = list(zip(*infections))
        self.infection_sum = list(map(sum, infections_zip))
        if max(self.infection_sum) > 24:
            self.lost = True

        if self.lost:
            self.turn_of = None
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
        self.outbreaks += self.board.infect(card.city.id_, 3)

        # Return drawn
        self.infection_deck.return_drawn()

    def infection_stage(self):
        forbiden = list()
        connections = [player.location.connections for player in self.players
                       if player.role == 2]
        forbiden = [city.id for city in connections] + [player.location for
                                                        player in self.players
                                                        if player.role == 2]
        cities = list()
        for i in range(self.board.infection_speeds[self.board.current_speed]):
            card = self.infection_deck.draw_card()

            if card is not None:
                if card.city.id_ not in forbiden:
                    self.outbreaks += self.board.infect(card.city.id_)
                    cities.append(self.board.locations[card.city.id_])
            else:
                return cities
        return cities

    def move_player(self, destination, player):
        if self.board.locations[destination] not in player.possible_moves():
            raise ValueError("City not available to move")
        player.move(self.board.locations[destination])

    def travel_player(self, destination, player):
        if self.board.locations[destination].name not in [city.name for city in
                                                          player.possible_travel_to()]:
            raise ValueError("City not available to travel")
        player.cards = [card for card in player.cards if
                        card.city.id != destination]
        player.move(self.board.locations[destination])

    def serialize(self):
        serial = self.board.serialize()
        serial.update({
            'players': [player.serialize() for player in self.players],
            'outbreaks': self.outbreaks,
            'cures': {COLORS[i]: self.cures[i] for i in range(4)},
            'turn': {'player': self.turn_of,
                     'remaining_actions': self.remaining_actions},
            'infections_sum': self.infection_sum,
            'infection_deck': self.infection_deck.serialize(),
            'player_deck': self.player_deck.serialize(),
            'lost': self.lost,
            'discard': self.discard
        })
        return serial


def deserialize(data: dict) -> Controller:
    deserialized_board = board.deserialize(data)
    deserialized_players = list()
    for serialized_player in data['players']:
        deserialized_players.append(
            player.deserialize(serialized_player, deserialized_board))
    deserialized_infection_deck = deck.deserialize(data.get('infection_deck'))
    deserialized_infection_deck.__class__ = InfectionDeck
    deserialized_player_deck = deck.deserialize(data.get('player_deck'))
    deserialized_player_deck.__class__ = PlayerDeck
    game = Controller(num_players=len(deserialized_players),
                      board=deserialized_board,
                      cures=[data.get('cures')[color] for color in COLORS],
                      lost=data.get('lost'),
                      infection_deck=deserialized_infection_deck,
                      infection_sum=data.get('infections_sum'),
                      player_deck=deserialized_player_deck,
                      outbreaks=data.get('outbreaks'),
                      players=deserialized_players,
                      turn_of=data.get('turn').get('player'),
                      remaining_actions=data.get('turn').get(
                          'remaining_actions'), discard=data.get('discard'))
    return game


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
    game_dict['player_deck'] = len(game_dict.get('player_deck').get('cards'))
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
    game.start_game()
    # Use a service account

    db = firestore.client()
    doc_ref_2 = db.collection('users_games').document(user_id).get()
    if doc_ref_2.exists:
        abort(400, "User already in a game")

    letters_and_digits = string.ascii_letters + string.digits
    game_id = ''.join((choice(letters_and_digits) for n in range(6)))

    doc_ref = db.collection('games').document(game_id)
    game_serialized = game.serialize()
    users = [None for n in range(1, num_players)]
    users[0] = user_id
    game_serialized.update({'users': users,
                            'password': str(
                                hashlib.sha256(password).hexdigest()),
                            'num_players': num_players,
                            'game_id': game_id})
    doc_ref.set(game_serialized)

    doc_ref_2 = db.collection('users_games').document(user_id)
    doc_ref_2.set({'game': game_id})

    return game_id


def do_action(game_id: str, action: dict, token_info: dict = None):
    try:
        user_id = token_info.get('primarysid')
    except:
        return abort(404, "Missing parameters")
    db = firestore.client()
    doc_ref_2 = db.collection('users_games').document(user_id).get().to_dict()
    if doc_ref_2.get('game') != game_id:
        return abort(400, "User is in a different game")
    game_dict = db.collection('games').document(game_id).get().to_dict()
    print(game_dict)

    game = deserialize(game_dict)

    if game_dict['users'][game.turn_of] != user_id:
        return abort(401, "Not your turn")
    # {'type':'move', 'data': {'destination': game.players[
    # game.turn_of].possible_moves()[0].id}}
    try:
        game.play_action(action)
    except ValueError as e:
        return abort(401, str(e))
    game_serialized = game.serialize()

    game_serialized.update({'users': game_dict.get('users'),
                            'password': game_dict.get('password'),
                            'num_players': game_dict.get('num_players'),
                            'game_id': game_id})
    db.collection('games').document(game_id).set(game_serialized)
    return game_serialized


def join_game(game_id: str, data: dict, token_info: dict):
    try:
        user_id = token_info.get('primarysid')
        password = data['password'].encode('utf-8')
    except:
        return abort(400, "Missing parameters")

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
    num_players = game_dict.get('num_players')

    if not len(users) < num_players:
        return abort(401, "Jogo lotado")

    doc_ref = db.collection('games').document(game_id)
    users.append(user_id)
    doc_ref.update({'users': users})

    doc_ref_2 = db.collection('users_games').document(user_id)
    doc_ref_2.set({'game': game_id})
    return game_id


def leave_game(game_id: str, token_info: dict):
    try:
        user_id = token_info.get('primarysid')
    except:
        return abort(404, "Missing parameters")
    db = firestore.client()
    doc_ref_2 = db.collection('users_games').document(user_id).get()
    if not doc_ref_2.exists:
        abort(400, "User not in a game")
    game_id_reg = doc_ref_2.to_dict().get('game')
    if game_id_reg is None:
        abort(400, "User not in a game")
    if game_id != game_id_reg:
        abort(400, "User not in this game")
    doc_ref_2 = db.collection('users_games').document(user_id).delete()
    return game_id


def live():
    db = firestore.client()
    doc_ref_2 = db.collection('games').get()
    return doc_ref_2 is None


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
