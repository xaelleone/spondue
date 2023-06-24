from Pieces import *
from Player import *
from Game import *
from CardNobles import *

playerKatie = HumanPlayer('Katie')
playerKevin = HumanPlayer('Kevin')
testgame1 = Game([playerKatie, playerKevin])    

print(testgame1.play_game())