class Player:
    def __init__(self):
        pass

    #takes in game state and returns an action
    def take_turn(self, game_state):
        pass


    #maybe takes in a dict of colors and numbers and adds/subtracts
    def update_chips(self, amount):
        pass
        # throw an exception if illegal
    
    #takes in a card on the board and adds it to player tableau
    def get_card_from_board(self, card):
        pass

    #takes in a card in player reserve and adds it to player tableau
    def get_card_from_reserve(self, card):
        pass

    #takes in a card on the board and adds it to player reserve
    def get_reserve_from_board(self, card):
        pass

    #takes in a noble and assigns it to the player
    def get_noble(self, noble):
        pass

    #totals the points for the player
    def get_points(self):
        pass