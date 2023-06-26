from Player import *
from Game import CHIP_LIMIT, ALL_CARDS
from Pieces import LIST_OF_COLORS
import random

class kdAIPlayer(Player):
    def __init__(self, name):
        super().__init__(name)
        self.turn_counter = 1
        self.care_about_this = []
        self.goal_card = ""
        self.turns_to_care_per_tier = {0: (0,10), 1: (6,15), 2: (8, 10000)}
        self.max_cost_per_tier = {0: 4, 1: 7, 2: 13}
        self.max_to_pay = 3
        self.too_far = 3

    def take_turn(self, game_state): #game state is a dict of game board, game bank, and other players' board / bank / reserve
        
        #1. determine which cards are worthwhile & update list of cards to care about
        def scan_good_cards(tier):
            if self.turn_counter > self.turns_to_care_per_tier[tier][0] and self.turn_counter < self.turns_to_care_per_tier[tier][1]:
                for card in game_state['board'][tier]:
                    if card.cost.total() <= self.max_cost_per_tier[tier]:
                        self.care_about_this.append(card)

        scan_good_cards(0)
        scan_good_cards(1)
        scan_good_cards(2)


        if len(self.care_about_this) == 0:
            return Turn(action = 'take',chips = Colorset(dict_of_colors={'R':1, 'W':1, 'G':1}))

        #2. determine goal card
        current_best_point = 0
        self.goal_card = self.care_about_this[0]

        for card in self.care_about_this: 
            if card not in game_state['board'][0] and card not in game_state['board'][1] and card not in game_state['board'][2]:
                self.care_about_this.remove(card)
            if card.points > current_best_point and card.tier != 0:
                self.goal_card = card  

        self.turn_counter += 1
        print("this is turn ", self.turn_counter)
        print("I care about", [card for card in self.care_about_this])
        print("My goal is currently", self.goal_card.cost.dict_of_colors)

        #3. obtain goal card if possible
        goal_colors = self.goal_card.cost
        board_colorset = Colorset(list_of_cards = self.tableau)
        needed_colors = goal_colors.subtract_to_zero(board_colorset)
        needed_colors = needed_colors.subtract_to_zero(self.chips)

        if needed_colors.total() <= self.gold:
            return Turn(action="buy", card=self.goal_card)
        
        
        #4. purchase cards that help goal from better cards if possible
        for card in self.care_about_this:
            if needed_colors.dict_of_colors[card.color] != 0 and self.can_buy(card):
                return Turn(action="buy", card=card)
        
        #5. purchase cards in general that help goal 
        for card in game_state['board'][0]:
            if needed_colors.dict_of_colors[card.color] != 0 and self.can_buy(card):
                return Turn(action="buy", card=card)

        #6. purchase cards that might help in general
        # TODO : implement caring about nobles
        for tier in range(NUMBER_OF_TIERS):
            for card in game_state['board'][tier]:
                effective_cost = card.cost.subtract_to_zero(board_colorset).total()
                if effective_cost < self.max_to_pay and self.can_buy(card) and needed_colors[card.color] != 0:
                    return Turn(action="buy", card=card)

        #7. reserve cards if you need too many of a color
        if max(needed_colors.dict_of_colors.values()) > self.too_far and len(self.reserve) < 3:
            most_achievable = self.care_about_this[0]
            for card in self.care_about_this:
                effective_cost = card.cost.subtract_to_zero(board_colorset).total()
                if effective_cost < most_achievable.cost.total():
                    most_achievable = card
            return Turn(action="reserve", card=card)

        #8. else, just take chips
        if max(needed_colors.dict_of_colors.values()) > self.too_far - 1:

            for color in LIST_OF_COLORS:
                if needed_colors.dict_of_colors[color] == 2 and game_state['bank'].dict_of_colors[color] > 3:
                    return Turn(action='take', chips = Colorset(dict_of_colors={color: 2}))

        taking_these = Colorset(initial_value=0)
        for color in LIST_OF_COLORS:
            if needed_colors.dict_of_colors[color] != 0 and game_state['bank'].dict_of_colors[color] !=0 and taking_these.total() < 3:
                taking_these = taking_these.combine(Colorset(dict_of_colors={color: 1}))
                print(taking_these)
        for color in LIST_OF_COLORS:
            if taking_these.total() < 3:
                taking_these = taking_these.combine(Colorset(dict_of_colors={color: 1}))
                print(taking_these.dict_of_colors)

        #9. if all else fails, should pass
        return Turn(action='take', chips=taking_these)

playerKatie = HumanPlayer('Katie')
playerKevin = kdAIPlayer('Kevin')
testgame1 = Game([playerKatie, playerKevin])    

print(testgame1.play_game())