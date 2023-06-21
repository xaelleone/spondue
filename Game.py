# stores the state for the splendor game, and simulates the game
from Player import *
from CardNobles import *
from CardNobles import *
import random

BANK_GIVEN_PLAYER_COUNT = {2:4, 3:5, 4:7}
GOLD_CHIPS = 5

class Game:
    # takes in a list of players in turn order & list of cards
    def __init__(self, players):

        #initialize players
        self.players = players

        #initialize bank as dict
        color_chip_count = BANK_GIVEN_PLAYER_COUNT[len(players)]
        self.bank = Colorset(initial_value=color_chip_count)
        self.gold_in_bank = GOLD_CHIPS

        #initialize decks as a list of 3 lists
        self.tier1deck = []
        self.tier2deck = []
        self.tier3deck =[]
        for card in ALL_CARDS:
            if card.tier == 1:
                self.tier1deck.append(card)
            elif card.tier == 2:
                self.tier2deck.append(card)
            elif card.tier == 3:
                self.tier3deck.append(card)

        #shuffle decks
        random.shuffle(self.tier1deck)
        random.shuffle(self.tier2deck)
        random.shuffle(self.tier3deck)

        #initialize board
        self.board = []

        #initialize nobles
        self.nobles = random.choices(ALL_NOBLES,k=3)
        
    # takes a player's turn. takes a player, asks for them to take their turn, and updates the game
    def player_turn(self, player):
        # player_action = self.player_list[player].take_turn(game_state)
        # self.update_game(player_action)
        pass

    # updates the game state given a player's turn action, including 
    def update_game(self, player, player_action):
        self.alter_player_state(player, player_action),
        self.update_board(player_action)
        pass

    # alters the player's state given their turn action. gives them cards, adds or deducts chips, etc.
    # this function should check the b  legality of player_action, and throw an Exception if illegal
    def alter_player_state(self, player, player_action):
        pass
        # if exception caught, cause player to lose

    # deals a new card given a player action, or does nothing if the player didn't take a card
    def update_board(self, player_action):
        pass

    # adds or reduces number of chips in the bank given a player action
    def update_chips(self, player_action):
        pass 

    # check if somebody has won
    # returns the player that won
    def check_win(self):
        pass


