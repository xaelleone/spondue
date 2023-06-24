# stores the state for the splendor game, and simulates the game
from Player import *
from Pieces import *
from CardNobles import *
import random
import itertools
import numpy as np

BANK_GIVEN_PLAYER_COUNT = {2:4, 3:5, 4:7}
GOLD_CHIPS = 5
CARDS_PER_TIER = 4
NUMBER_OF_TIERS = 3
WINNING_POINTS = 15
CHIP_LIMIT = 10

class Game:
    # takes in a list of players in turn order & list of cards
    def __init__(self, players):

        #initialize players
        self.players = players

        #initialize bank as dict
        color_chip_count = BANK_GIVEN_PLAYER_COUNT[len(players)]
        self.bank = Colorset(initial_value=color_chip_count)
        self.gold_in_bank = GOLD_CHIPS

        # initialize decks by grouping cards by tier
        # tiers have names which are 0-indexed numbers
        self.decks = [list(g) for k, g in itertools.groupby(ALL_CARDS, lambda x: x.tier)]

        #shuffle decks
        for deck in self.decks:
            random.shuffle(deck)

        #initialize board
        self.board = []
        for tier in range(len(self.decks)):
            # first, start an initial empty list for that tier
            self.board.append([])
            for _ in range(CARDS_PER_TIER):
                self.draw_new_card(tier)

        #initialize nobles
        self.nobles = random.choices(ALL_NOBLES,k=3)
        
    # takes a player's turn. takes a player, asks for them to take their turn, and updates the game
    def player_turn(self, player):
        # player_action = self.player_list[player].take_turn(game_state)
        # self.update_game(player_action)
        pass

    # updates the game state given a player's turn action, including 
    def update_game(self, player, player_action):
        if player_action.action == 'reserve':
            self.update_gold_on_reserve(player)
            if player_action.topdeck is not None:
                if not self.decks[player_action.topdeck]:
                    raise IllegalMoveException(f'{player.name} tried to topdeck from empty deck {player_action.topdeck}')
                reservee = self.decks[player_action.topdeck].pop()
                player.get_reserve_from_board(reservee)
            else:
                reservee = player_action.card
                if reservee in self.board[reservee.tier]:
                    self.board[reservee.tier].remove(reservee)
                    self.draw_new_card(reservee.tier)
                    player.get_reserve_from_board(reservee)
                else:
                    raise IllegalMoveException(f'{player.name} tried to reserve unavailable card')
        elif player_action.action == 'take':
            self.check_whether_chip_taking_is_allowed(player, player_action)
            # transfer those chips to the player, to see if it is allowed
            self.bank = self.bank.subtract_to_zero(player_action.chips)
            player.chips = player.chips.combine(player_action.chips)
        elif player_action.action == 'buy':
            buyee = player_action.card
            if buyee in player.reserve:
                self.pay_chips(player, buyee)
                player.get_card_from_reserve(buyee)
            elif buyee in self.board[buyee.tier]:
                self.pay_chips(player, buyee)
                player.get_card_from_board(buyee)
                self.board[buyee.tier].remove(buyee)
                self.draw_new_card(buyee.tier)
            else:
                raise IllegalMoveException(f'{player.name} tried to buy unavailable card')

    # deals one new card from the deck of that tier if it exists, and puts it on the board
    def draw_new_card(self, tier):
        # only pop a card if there is one
        if self.decks[tier]:
            new_card = self.decks[tier].pop()
            self.board[tier].append(new_card)
        
    # updates everybody's gold when a player tries to reserve
    # gives them a gold if there is one
    def update_gold_on_reserve(self, player):
        if self.gold_in_bank > 0:
            self.gold_in_bank -= 1
            player.gold += 1

    # takes in a player and the card they want to buy, 
    # deducts the appropriate chips and puts them in the bank
    # throws an exception if the player can't afford the card     
    def pay_chips(self, player, buyee):
        discounted_cost = buyee.cost.subtract_to_zero(Colorset(list_of_cards=player.tableau))
        gold_allocation = discounted_cost.subtract_to_zero(player.chips)
        if gold_allocation.total() < player.gold:
            raise IllegalMoveException(f'{player.name} cannot afford a card with cost {buyee.cost.dict_of_colors}')
        
        regular_chip_cost = discounted_cost.subtract_to_zero(gold_allocation)
        player.chips = player.chips.subtract_to_zero(regular_chip_cost)
        self.bank = self.bank.combine(regular_chip_cost)

        gold_cost = gold_allocation.total()
        player.gold -= gold_cost
        self.gold_in_bank += gold_cost

    def check_whether_chip_taking_is_allowed(self, player, player_action):
        # convoluted logic to check if player only took two chips if there were four in that pile
        taken_chips_dict = player_action.chips.dict_of_colors
        flipped_dict = dict([count, color] for color, count in taken_chips_dict.items())
        if 2 in flipped_dict and self.bank.get_amount(flipped_dict[2]) < 4:
            raise IllegalMoveException(f'{player.name} tried to take 2 chips from a pile where there would be fewer than two left')
        
        # check if player took chips that break the bank
        if not player_action.chips.check_requirement(self.bank):
            raise IllegalMoveException(f'{player.name} tried to take chips which are not in the bank')
        
        # check that the player is not asking to have more than ten chips
        if player.chips.combine(player_action.chips).total() + player.gold > CHIP_LIMIT:
            raise IllegalMoveException(f'{player.name} tried to have more than ten chips')

    # check if somebody has won
    # returns True if someone has exceeded WINNING_POINTS, False otherwise
    def check_game_will_end_this_round(self):
        return any([player.get_points() >= WINNING_POINTS for player in self.players])

    # upon the game ending, find out who won the game
    # it is the person who who has the most points, with ties broken by fewest cards
    def find_winner(self):
        # clever function that adds points plus half the reciprocal of cards
        hybrid_score_function = lambda x: x.get_points() + 0.5 / (1 + len(x.tableau))
        hybrid_scores = [hybrid_score_function(player) for player in self.players]
        winner_index = np.argmax(hybrid_scores)
        return self.players[winner_index]



