from Player import *
from Pieces import *
import numpy as np

# AI player based on computing the Card strength (CS) and Color valuability (CV)
class CscvAIPlayer(Player):
    def __init__(self, points_weight = 1, noble_weight=0, color_valuability_weight=20, cost_weight=0.2, card_care_threshold=0, quadratic_cost_weight=1, name='Cscv'):
        super().__init__(name)
        self.color_valuability = Colorset(initial_value = 0.2)
        self.card_strength_weights = [points_weight, noble_weight, color_valuability_weight, -1 * cost_weight]
        self.card_care_threshold = card_care_threshold
        self.quadratic_cost_weight = quadratic_cost_weight
        self.n_iterations = 5

    def take_turn(self, game_state):
        self.cscv_compute(game_state['board'])
        flat_card_list = [card for tier in game_state['board'] for card in tier]
        cards_by_quality = sorted(flat_card_list, key=self.compute_card_strength, reverse=True)
        for candidate_buyee in cards_by_quality:
            #print(candidate_buyee.points, candidate_buyee.color, candidate_buyee.cost.dict_of_colors)
            #print('value this card at ', self.compute_card_strength(candidate_buyee))
            if candidate_buyee.cost.check_requirement(self.get_purchasing_power()):
                return Turn('buy', card=candidate_buyee)
        # if we got here, then we should take chips
        candidate_chip_takings = self.get_all_possible_chip_takings(game_state['bank'])
        chip_taking_quality = lambda x: x.dot_product(self.color_valuability)
        best_chip_takings = sorted(candidate_chip_takings, key=chip_taking_quality, reverse=True)
        return Turn('take', chips=best_chip_takings[0])

    # cost of a card, modulo our tableau bonos
    def discounted_cost(self, card: Card):
        return card.cost.subtract_to_zero(self.get_purchasing_power())

    def compute_card_strength(self, card: Card):
        noble_component = 0
        #TODO: compute noble component
        card_color_component = self.color_valuability.get_amount(card.color)
        # TODO: parametrize this quadratic
        cost_component = self.quadratic_cost_weight * self.discounted_cost(card).total() ** 2 + self.discounted_cost(card).total()
        return np.dot(self.card_strength_weights, [card.points, noble_component, card_color_component, cost_component])
    
    def recompute_color_valuability(self, board):
        cumulative_color_valuability = Colorset(initial_value=1)
        for tier in board:
            for card in tier:
                card_color_strengths = self.discounted_cost(card).multiply_by_constant(max(self.card_care_threshold, self.compute_card_strength(card)))
                cumulative_color_valuability = cumulative_color_valuability.combine(card_color_strengths)
        
        scale = 1 / cumulative_color_valuability.total()
        self.color_valuability = cumulative_color_valuability.multiply_by_constant(scale)

    def cscv_compute(self, board):
        for _ in range(self.n_iterations):
            self.recompute_color_valuability(board)
            #print(f'color valuability at {self.color_valuability.dict_of_colors}')
