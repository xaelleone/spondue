# stores the state for the splendor game, and simulates the game
class Game:
    def __init__(self):
        pass

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
    # this function should check the legality of player_action, and throw an Exception if illegal
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


