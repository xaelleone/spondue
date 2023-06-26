from Player import *
from Pieces import *
import numpy as np

# AI player based on computing the Card strength (CS) and Color valuability (CV)
class CscvAIPlayer(Player):
    def __init__(self, noble_weight=0, color_valuability_weight=1, cost_weight=1, buy_threshold=0, name='Cscv'):
        super().__init__(name)
        self.color_valuability = Colorset(initial_value = 0.2)
        self.card_strength_weights = [noble_weight, color_valuability_weight, cost_weight]
        self.buy_threshold = buy_threshold
        self.n_iterations = 20

    def take_turn(self, game_state):
        self.cscv_compute(game_state['board'])
        flat_card_list = [card for tier in game_state['board'] for card in tier]
        cards_by_quality = sorted(flat_card_list, key=self.compute_card_strength, reverse=True)
        for candidate_buyee in cards_by_quality:
            if self.compute_card_strength(candidate_buyee) > self.buy_threshold:
                if candidate_buyee.check_requirement(self.get_purchasing_power()):
                    return Turn('buy', card=candidate_buyee)
            else:
                break
        

    # cost of a card, modulo our tableau bonos
    def discounted_cost(self, card: Card):
        return card.cost.subtract_to_zero(Colorset(list_of_cards=self.tableau))

    def compute_card_strength(self, card: Card):
        noble_component = 0
        card_color_component = self.color_valuability.get_amount(card.color)
        cost_component = self.discounted_cost(card).dot_product(self.color_valuability)
        return np.dot(self.card_strength_weights, [noble_component, card_color_component, cost_component])
    
    def recompute_color_valuability(self, board):
        cumulative_color_valuability = Colorset(initial_value=0)
        for tier in board:
            for card in tier:
                card_color_strengths = self.discounted_cost(card).multiply_by_constant(self.compute_card_strength(card))
                cumulative_color_valuability = cumulative_color_valuability.combine(card_color_strengths)
        self.color_valuability = cumulative_color_valuability

    def cscv_compute(self, board):
        for _ in range(self.n_iterations):
            self.recompute_color_valuability(board)
