from Game import *
from CscvAIPlayer import *
from GreedyRandomChipGrabberAIPlayer import *
from collections import defaultdict
import random
import numpy as np

MAX_PARAMS_TO_MUTATE = 3
MUTATION_STDDEV = 1
MAX_GENERATIONS = 20
GENERATION_SIZE = 10
MAX_GAMES_AGAINST_RANDOM = 100

def mutate(params):
    new_params = params.copy()
    # pick a random number of params
    mutated_params = random.sample(list(params.keys()), random.randint(0, MAX_PARAMS_TO_MUTATE))

    for mutatee in mutated_params:
        new_params[mutatee] += np.random.normal(scale=MUTATION_STDDEV)

    return new_params

def offspring(parents_params, generation_size):
    param_list = parents_params[0].keys()

    children = []
    for _ in range(generation_size):
        pct_genes = np.random.dirichlet([1] * len(parents_params), len(param_list))
        new_params = dict([(param, np.dot(pct_genes[i,:], [parent[param] for parent in parents_params])) for i, param in enumerate(param_list)])
        mutated_new_params = mutate(new_params)
        children.append(mutated_new_params)
    
    return children

def get_player_from_params(params, id):
    return CscvAIPlayer(**params, name=id)

def get_player_id(generation, index):
    return f'generation {generation}, index {index}'

def starting_seed():
    return {
        'points_weight': 1,
        'noble_weight': 0,
        'color_valuability_weight': 20, 
        'cost_weight': 0.2, 
        'card_care_threshold': 0, 
        'quadratic_cost_weight': 1
    }

def simulate():
    parents = [starting_seed()]
    opponent = GreedyRandomChipGrabberAIPlayer()
    scores = defaultdict(list)
    for i in range(MAX_GENERATIONS):
        children = offspring(parents, GENERATION_SIZE)
        for j in range(len(children)):
            player_id = get_player_id(i, j)
            player = get_player_from_params(children[j], player_id)
            score = 0
            for k in range(MAX_GAMES_AGAINST_RANDOM):
                player.reset()
                opponent.reset()
                matchup = Game([player, opponent])
                winner = matchup.play_game(verbose=False)
                if winner == player_id:
                    score += 1
            print(f'{player_id} achieved {score}')
            print(children[j])
            scores[i].append(score)
        top_children = np.argpartition(scores[i], -2)[-2:]
        parents = [children[j] for j in top_children]
    

simulate()  
    

