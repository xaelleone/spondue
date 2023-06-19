from Pieces import *
from Player import *
import pytest

card1 = Card({'W':1,'B':2},'R',1,1)
card2 = Card({'W':1,'B':2},'W',3,2)
card3 = Card({'W':1,'B':2},'U',4,3)
noble1 = Noble({'R':3},3)
noble2 = Noble({'R':1},300)
noble3 = Noble({'R':1, 'W':2},3)

def test_noble_requirements():
    assert not noble1.check_requirements([card1])
    assert not noble2.check_requirements([card2])
    assert noble2.check_requirements([card1])
    assert noble2.check_requirements([card1,card2])
    assert noble1.check_requirements([card1,card1,card1])
    assert not noble1.check_requirements([])

def test_points_for_player():
    player1 = Player()
    player1.tableau = [card1]
    assert player1.get_points() == 1
    player1.nobles = [noble1, noble2]
    assert player1.get_points() == 304
    player2 = Player()
    assert player2.get_points() == 0
    player2.tableau = [card1, card1, card3]
    assert player2.get_points() == 6

def test_adding_card_for_player():
    player1 = Player()
    player1.get_card_from_board(card1)
    assert player1.tableau == [card1]
    with pytest.raises(IllegalMoveException):
        player1.get_card_from_reserve(card1)
    player1.reserve = [card2]
    player1.get_card_from_reserve(card2)
    assert player1.reserve == []
    assert card2 in player1.tableau
