from Player import *
from Game import CHIP_LIMIT
from Pieces import LIST_OF_COLORS
import random

# extremely simple AI that:
# if it can buy a card, buys the card worth the most points
# otherwise, takes random chips
class GreedyRandomChipGrabberAIPlayer(Player):
    def __init__(self, name='GreedyRandomChipGrabberAI'):
        super().__init__(name)

    def take_turn(self, game_state):
        for tier in game_state['board'][::-1]:
            for card in sorted(tier, key=lambda x: x.points, reverse=True):
                if card.cost.check_requirement(self.get_purchasing_power()):
                    return Turn('buy', card=card)
        else:
            bank = game_state['bank']
            legal_moves = self.get_all_possible_chip_takings(bank)
            return Turn('take', chips=random.choice(legal_moves))

