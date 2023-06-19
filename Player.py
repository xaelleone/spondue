from Game import *
from Pieces import *

class Player:
    def __init__(self):
        self.chips = dict(zip(LIST_OF_COLORS, [0]*len(LIST_OF_COLORS)))
        self.tableau = []
        self.reserve = []
        self.nobles = []

    #takes in game state and returns an action
    def take_turn(self, game_state):
        pass


    #maybe takes in a dict of colors and numbers and adds/subtracts
    def update_chips(self, amount):        
        pass
        # throw an exception if illegal
    
    #takes in a card on the board and adds it to player tableau
    def get_card_from_board(self, card):
        self.tableau.append(card)

    #takes in a card in player reserve and adds it to player tableau
    def get_card_from_reserve(self, card):
        if card not in self.reserve:
            raise IllegalMoveException()
        self.tableau.append(card)
        self.reserve.remove(card)


    #takes in a card on the board and adds it to player reserve
    def get_reserve_from_board(self, card):
        pass

    #takes in a noble and assigns it to the player
    def get_noble(self, noble):
        pass

    #totals the points for the player
    def get_points(self):
        card_points = sum([card.points for card in self.tableau])
        noble_points = sum([noble.points for noble in self.nobles])
        return card_points + noble_points