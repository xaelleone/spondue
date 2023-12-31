from Pieces import *
import itertools
from constants import *

class Player:
    def __init__(self, name):
        self.name = name
        self.reset()

    def reset(self):
        self.chips = Colorset(initial_value=0)
        self.tableau = []
        self.reserve = []
        self.nobles = []
        self.gold = 0

    # takes in game state and returns an action
    # parent version which is never called
    def take_turn(self, game_state):
       return Turn('')
   

    #takes in a card on the board and adds it to player tableau
    def get_card_from_board(self, card):
        self.tableau.append(card)
        #may need exception if card not on board


    #takes in a card in player reserve and adds it to player tableau
    def get_card_from_reserve(self, card):
        if card not in self.reserve:
            raise IllegalMoveException()
        self.tableau.append(card)
        self.reserve.remove(card)


    #takes in a card on the board and adds it to player reserve
    def get_reserve_from_board(self, card):
        if len(self.reserve) > 3: #if reserve is full
            raise IllegalMoveException()
        self.reserve.append(card)
        #may need exception if card not on board


    #takes in a noble and assigns it to the player
    def get_noble(self, noble):
        self.nobles.append(noble)
        #may need exception if card not on board


    #totals the points for the player
    def get_points(self):
        card_points = sum([card.points for card in self.tableau])
        noble_points = sum([noble.points for noble in self.nobles])
        return card_points + noble_points

    # helper function for AIs that returns a list of possible colorsets
    def get_all_possible_chip_takings(self, bank: Colorset):
        possible_actions = []

        chips_takeable = min(3, CHIP_LIMIT - self.chips.total())
        if chips_takeable >= 2:
            for color in LIST_OF_COLORS:
                if bank.get_amount(color) >= 4:
                    candidate_action = Colorset(dict_of_colors={color: 2})
                    possible_actions.append(candidate_action)
        
        available_colors = [color for color in LIST_OF_COLORS if bank.get_amount(color)]
        color_combos = itertools.combinations(available_colors, min(chips_takeable, len(available_colors)))
        single_chip_actions = [Colorset(dict_of_colors=dict(zip(colors_picked, [1] * chips_takeable))) for colors_picked in color_combos]

        possible_actions.extend(single_chip_actions)

        return possible_actions


    # helper function that computes how much a player can buy
    def get_purchasing_power(self):
        return Colorset(list_of_cards = self.tableau).combine(self.chips)

    #helper function that returns True if a card is buyable
    def can_buy(self, card):
        return card.cost.check_requirement(self.get_purchasing_power())

class Turn():
    VALID_INPUT = ['buy', 'take', 'reserve']
    # action is a string, buy / take / reserve
    # card is a card object, for either buy or reserve
    # chips is a colorset to get from the bank, only valid for take
    # topdeck is an int 0, 1, or 2 depending on the tier, only valid for reserves
    def __init__(self, action, card = None, chips = None, topdeck = None):
        if action not in Turn.VALID_INPUT:
            raise IllegalMoveException("Turn type not valid")

        #checking validity if buying
        if action == 'buy':
            if card is None or chips is not None or topdeck is not None:
                raise IllegalMoveException("Buying with wrong set of arguments")
        
        #checking validity if reserving
        elif action == 'reserve':        
            if chips is not None:
                raise IllegalMoveException("Can't take chips while reserving")
            
            if topdeck is not None:
                if card is not None or topdeck not in range(NUMBER_OF_TIERS):
                    raise IllegalMoveException("Can't topdeck with cards or tier not valid")
            
            if card is not None and topdeck is not None:
                raise IllegalMoveException("Can't reserve card and topdeck")

        elif action == 'take':
            if chips is None or card is not None or topdeck is not None:
                raise IllegalMoveException("Can't take chips and do other things")

            taken_vals = list(chips.dict_of_colors.values())

            if 2 in taken_vals:
                if sum(taken_vals) != 2 or min(taken_vals) < 0:
                    raise IllegalMoveException("Can't take this number of chips")
            else:
                if (sum(taken_vals) > 3 or (max(taken_vals) > 1)) or min(taken_vals) < 0:
                    raise IllegalMoveException("Can't take this number of chips")

        self.chips = chips
        self.topdeck = topdeck
        self.action = action
        self.card = card

    
class HumanPlayer(Player):
    def __init__(self, name):
        super().__init__(name)

    def take_turn(self, game_state): #game state is a dict of game board, game bank, and other players' board / bank / reserve
        # TODO: should in theory show the other players' things, which is in game_state

        valid_input = 'brt'

        action = input("Would you like to buy (b), reserve (r), or take chips from the bank (t)? ")
        while action not in valid_input or len(action) != 1:
            action = input("Your options are buy (b), reserve (r), or take (t). ")
        
        if action == 'b':
            from_res_ask = int(input("Will you buy from reserve? 1 or 0: "))
            if from_res_ask:
                res_index = int(input("Index of the card in your reserve: "))
                return Turn(action = 'buy', card = self.reserve[res_index])
            tier_index = int(input("Specify the tier (0-2) of the card you want: "))
            if tier_index not in range(NUMBER_OF_TIERS):
                raise IllegalMoveException("This was not a valid tier.")
            buy_index = int(input("Index (0-3) of the card you want: "))
            if buy_index not in range(CARDS_PER_TIER):
                raise IllegalMoveException("That is not a valid index.")
            return Turn(action = 'buy', card = game_state['board'][tier_index][buy_index])
            
        elif action == 'r':
            topdeck_ask = int(input("Will you topdeck? 1 or 0: "))
            if topdeck_ask:
                topdeck_tier = int(input("Which tier do you want, 0 1 or 2: "))
                return Turn(action='reserve', topdeck = topdeck_tier)
            tier_index = int(input("Specify the tier (0-2) of the card you want: "))
            if tier_index not in range(NUMBER_OF_TIERS):
                raise IllegalMoveException("This was not a valid tier.")
            buy_index = int(input("Index (0-3) of the card you want: "))
            if buy_index not in range(CARDS_PER_TIER):
                raise IllegalMoveException("That is not a valid index.")

            return Turn(action = 'reserve', card = game_state['board'][tier_index][buy_index])

        elif action == 't':
            w = int(input("How many white chips would you like? "))
            b = int(input("How many black chips would you like? "))
            r = int(input("How many red chips would you like? "))
            u = int(input("How many blue chips would you like? "))
            g = int(input("How many green chips would you like? "))
            color_dict = {'R':r,'G':g,'B':b,'W':w,'U':u}
    
            return Turn(action = "take", chips = Colorset(dict_of_colors=color_dict))