from Pieces import *
from Player import *
from CardNobles import *
import pytest

expensiveCard = Card(Colorset(dict_of_colors={'W':100}),'R',1,1)
redRedCard = Card(Colorset(dict_of_colors={'R':1}),'R',1,1)
blueRedCard = Card(Colorset(dict_of_colors={'R':2,'U':2}),'U',2,3)

erikTheRed = Noble(Colorset(dict_of_colors={'R':1}),3)
haraldBluetooth = Noble(Colorset(dict_of_colors={'U':1}),300)
redBlueMan = Noble(Colorset(dict_of_colors={'R':1,'U':1}),3)

def test_noble_requirements():
    assert not erikTheRed.check_requirement([blueRedCard])
    assert redBlueMan.check_requirement([redRedCard, blueRedCard])
    assert not erikTheRed.check_requirement([])

def test_points_for_player():
    player1 = Player()
    player1.tableau = [redRedCard]
    assert player1.get_points() == 1
    player1.nobles = [erikTheRed, haraldBluetooth]
    assert player1.get_points() == 304
    player2 = Player()
    assert player2.get_points() == 0

def test_adding_card_for_player():
    player1 = Player()
    player1.get_card_from_board(redRedCard)
    assert player1.tableau == [redRedCard]
    with pytest.raises(IllegalMoveException):
        player1.get_card_from_reserve(redRedCard)
    player1.reserve = [blueRedCard]
    player1.get_card_from_reserve(blueRedCard)
    assert player1.reserve == []
    assert blueRedCard in player1.tableau

def test_colorset_combination():
    player1 = Player()
    player1.chips = Colorset(initial_value=3)
    with pytest.raises(IllegalMoveException):
        player1.chips = player1.chips.subtract(expensiveCard.cost)
    player1.chips = player1.chips.combine(expensiveCard.cost)
    assert player1.chips.dict_of_colors['W'] == 103
