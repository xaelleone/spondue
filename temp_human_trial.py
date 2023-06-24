from Pieces import *
from Player import *
from Game import *
from CardNobles import *

testgame1 = Game(['Alice','Bob'])    
testgamestate = {'board':testgame1.board, 'bank':testgame1.bank}
human = HumanPlayer('Katie')

human.take_turn(testgamestate)