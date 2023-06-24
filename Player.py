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
    # def take_turn(self, game_state):
    #    pass
   

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

class Turn():
    valid_input = ['take', 'buy', 'reserve']
    def __init__(self, action, card = None, chips = None):
        if action not in valid_input:
            raise IllegalMoveException()
        self.action = action

        if action == 'take':
            return 
    

class HumanPlayer(Player):
    def __init__(self):
        super().__init__()

    def take_turn(self, game_state):
        print(game_state['board'])
        print(game_state['bank'])
        
        action = Turn(input("Would you like to 'buy', 'reserve', or 'take' chips from the bank?"))
        while action not in valid_input and len(action) != 1:
            action = input("Your options are buy (b), reserve (r), or take (t).")
        
        if action == 'b':
            buy_index = input("Which card would you like to buy?")
            return game_state[board][buy_index]
            
        elif action == 'r':
            print(game_state.board)

            res_index = input("Which card would you like to reserve?")

            return game_state.board[res_index]

        elif action == 't':
            print(game_state.bank.dict_of_colors)
            r = input("How many red chips would you like?")
            g = input("How many green chips would you like?")
            b = input("How many black chips would you like?")
            w = input("How many white chips would you like?")
            u = input("How many blue chips would you like?")
            color_dict = {'R':r,'G':g,'B':b,'W':w,'U':u}
    
            return ("t",Colorset(dict_of_colors=color_dict))
