from Game import *
from Player import *
from GreedyRandomChipGrabberAIPlayer import *

human = HumanPlayer('you')
game = Game([GreedyRandomChipGrabberAIPlayer(), GreedyRandomChipGrabberAIPlayer('other')])

print(game.play_game(verbose=True))