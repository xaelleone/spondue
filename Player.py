from Game import *
from Pieces import *

class Player:
    def __init__(self):
        self.chips = Colorset(initial_value=0)
        self.tableau = []
        self.reserve = []
        self.nobles = []
        self.gold = 0


    #takes in game state and returns an action
    def take_turn(self, game_state):
        pass
   

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