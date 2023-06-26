from Game import *
from Player import *
from GreedyRandomChipGrabberAIPlayer import *
from CscvAIPlayer import *
from collections import defaultdict

def round_robin(players, matches_per_pairing):
    score = defaultdict(int)

    for i, player1 in enumerate(players):
        for j, player2 in enumerate(players):
            if i > j:
                for k in range(matches_per_pairing):
                    player1.reset()
                    player2.reset()
                    matchup = Game([player1, player2])
                    winner = matchup.play_game(verbose=True)
                    score[winner] += 1

    return score

players = [GreedyRandomChipGrabberAIPlayer(), CscvAIPlayer()]
#players = [HumanPlayer('me'), CscvAIPlayer()]
print(round_robin(players, 5))