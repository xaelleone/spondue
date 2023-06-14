from Pieces import *

card1 = Card({'W':1,'B':2},'R',1,5)
card2 = Card({'W':1,'B':2},'W',1,5)
card3 = Card({'W':1,'B':2},'U',1,5)
noble1 = Noble({'R':3},3)
noble2 = Noble({'R':1},3)
noble3 = Noble({'R':1, 'W':2},3)

def test_noble_requirements():
    assert not noble1.check_requirements([card1])
    assert not noble2.check_requirements([card2])
    assert noble2.check_requirements([card1])
    assert noble2.check_requirements([card1,card2])
    assert noble1.check_requirements([card1,card1,card1])
    assert not noble1.check_requirements([])
