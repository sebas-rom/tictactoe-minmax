"""Games or Adversarial Search (Chapter 5)"""

import copy
import itertools
import random
from collections import namedtuple
import game_management
import numpy as np



GameState = namedtuple('GameState', 'to_move, utility, board, moves')
StochasticGameState = namedtuple('StochasticGameState', 'to_move, utility, board, moves, chance')

def minmax_decision(state, game):
    return None

from collections import deque
from copy import deepcopy

# Example usage:
# Assuming you have the TicTacToe game class with methods is_terminal, get_legal_moves, and make_move.
# current_state = GameState(to_move=1, utility=0, board=None, moves=None)
# tree = generate_all_moves_tree(current_state, TicTacToe())
# print(tree)

def actions(state):
    """
    Generate possible actions for the current state.
    """
    # Implement your logic to generate possible actions based on the current state.
    # This will depend on the structure of your GameState.
    # Return a list of valid moves/actions.
    return state.moves

def minmax_decision(state, game):
    """Given a state in a game, calculate the best move by searching
    forward all the way to the terminal states. [Figure 5.3]"""

    def max_value(state):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = -np.inf
        for a in actions(state):
            v = max(v, min_value(game.result(state, a)))
        return v

    def min_value(state):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = np.inf
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a)))
        return v

    # Body of minmax_decision:
    return max(game.actions(state), key=lambda a: min_value(game.result(state, a)))


    #if check_gamestatus(cells) !=4: 
        #return check_gamestatus(cells)
        
        
   