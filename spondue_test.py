from Pieces import *
from Player import *
from Game import *
from CardNobles import *
import pytest

expensiveCard = Card(Colorset(dict_of_colors={'W':100,'B':100,'U':100,'R':100,'G':100}),'R',1,0)
redRedCard = Card(Colorset(dict_of_colors={'R':1}),'R',1,0)
blueRedCard = Card(Colorset(dict_of_colors={'R':2,'U':2}),'U',2,2)

erikTheRed = Noble(Colorset(dict_of_colors={'R':1}),3)
haraldBluetooth = Noble(Colorset(dict_of_colors={'U':1}),300)
redBlueMan = Noble(Colorset(dict_of_colors={'R':1,'U':1}),3)

def test_noble_requirements():
    assert not erikTheRed.check_requirement([blueRedCard])
    assert redBlueMan.check_requirement([redRedCard, blueRedCard])
    assert not erikTheRed.check_requirement([])

def test_points_for_player():
    player1 = Player('Mallory')
    player1.tableau = [redRedCard]
    assert player1.get_points() == 1
    player1.nobles = [erikTheRed, haraldBluetooth]
    assert player1.get_points() == 304
    player2 = Player('Polar Bear')
    assert player2.get_points() == 0

def test_adding_card_for_player():
    player1 = Player('Mallory')
    player1.get_card_from_board(redRedCard)
    assert player1.tableau == [redRedCard]
    with pytest.raises(IllegalMoveException):
        player1.get_card_from_reserve(redRedCard)
    player1.reserve = [blueRedCard]
    player1.get_card_from_reserve(blueRedCard)
    assert player1.reserve == []
    assert blueRedCard in player1.tableau

def test_colorset_combination():
    player1 = Player('Mallory')
    player1.chips = Colorset(initial_value=3)
    player1.chips = player1.chips.subtract_to_zero(expensiveCard.cost)
    assert sum(list(player1.chips.dict_of_colors.values())) == 0
    player1.chips = player1.chips.combine(expensiveCard.cost)
    assert player1.chips.dict_of_colors['W'] == 100
    player1.chips = player1.chips.subtract_to_zero(redRedCard.cost)
    assert player1.chips.dict_of_colors['R'] == 99


def test_game_init():
    testgame1 = Game([Player('Alice'), Player('Bob')])
    assert len(testgame1.nobles) == 3 
    assert len(testgame1.decks[0]) == 36
    assert testgame1.bank.dict_of_colors['W'] == 4
    testgame2 = Game([Player('Alice'), Player('Bob'), Player('Eve')])
    # test that decks are shuffled
    assert testgame2.decks[0] != testgame1.decks[0]

# test whether the game ends when someone reaches 15 points
def test_game_ends_at_right_time():
    playerAlice = Player('Alice')
    testgame1 = Game([playerAlice, Player('Bob')])
    assert not testgame1.check_game_will_end_this_round()
    # check that game will end once alice gets a very very valuable noble
    playerAlice.get_noble(haraldBluetooth)
    assert testgame1.check_game_will_end_this_round()

# test whether the winner is determined correctly when the game ends
def test_winner_correctly_determined():
    playerAlice = Player('Alice')
    playerBob = Player('Bob')
    # first test case, different number of points
    game = Game([playerAlice, playerBob])
    playerBob.get_card_from_board(blueRedCard)
    assert game.find_winner() == playerBob
    # second test case, same points using cards as tiebreak
    playerAlice.get_card_from_board(expensiveCard)
    playerAlice.get_card_from_board(redRedCard)
    assert game.find_winner() == playerBob


def test_pay_chips():
    playerAlice = Player('Alice')
    playerBob = Player('Bob')
    game = Game([playerAlice, playerBob])

    #first case
    playerAlice.gold = 500
    game.pay_chips(playerAlice, expensiveCard)
    assert game.gold_in_bank == 505
    assert playerAlice.gold == 0 
    
    with pytest.raises(IllegalMoveException):
        game.pay_chips(playerAlice, game.board[0][1])
    
    #second case
    playerBob.chips = Colorset(initial_value=4)

    with pytest.raises(IllegalMoveException):
        game.pay_chips(playerBob, expensiveCard) #bob is poor
    
    playerBob.gold = 500 #bob spends only gold
    game.pay_chips(playerBob, expensiveCard)
    assert game.gold_in_bank == 985
    assert playerBob.gold == 20
    assert game.bank.dict_of_colors['R'] == 8

    rando_tier_1_card = game.board[0][1] #bob has enough gold to afford any tier 1
    game.pay_chips(playerBob, rando_tier_1_card)

    playerBob.chips = playerBob.chips.combine(Colorset(initial_value=1000)) #bob shouldn't spend gold
    old_gold = game.gold_in_bank
    game.pay_chips(playerBob, rando_tier_1_card)
    new_red_total = 8 + rando_tier_1_card.cost.dict_of_colors['R']
    assert game.bank.dict_of_colors['R'] == new_red_total
    assert game.gold_in_bank == old_gold

    

    