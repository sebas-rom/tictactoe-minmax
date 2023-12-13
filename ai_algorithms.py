"""Games or Adversarial Search (Chapter 5)"""

import copy
import itertools
import random
from collections import namedtuple

import numpy as np



GameState = namedtuple('GameState', 'to_move, utility, board, moves')
StochasticGameState = namedtuple('StochasticGameState', 'to_move, utility, board, moves, chance')


def minmax_decision(state, game):
    return None

from collections import deque
from copy import deepcopy

def generate_all_moves_tree(current_state, game, max_depth=3):
    """
    Generates a tree of all possible next moves for each player up to a certain depth.
    Args:
    - current_state: The current game state.
    - game: The game instance (e.g., TicTacToe).
    - max_depth: Maximum depth to explore in the tree.

    Returns:
    - A tree of all possible next moves.
    """

    def generate_moves_recursive(state, current_depth, player):
        if current_depth == 0 or game.is_terminal(state):
            return state

        possible_moves = game.get_legal_moves(state)
        next_states = []

        for move in possible_moves:
            next_state = game.make_move(state, move, player)
            next_states.append(generate_moves_recursive(next_state, current_depth - 1, 3 - player))

        return (state, next_states)

    root = generate_moves_recursive(current_state, max_depth, current_state.to_move)
    return root

# Example usage:
# Assuming you have the TicTacToe game class with methods is_terminal, get_legal_moves, and make_move.
# current_state = GameState(to_move=1, utility=0, board=None, moves=None)
# tree = generate_all_moves_tree(current_state, TicTacToe())
# print(tree)

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
        
        
    def actions(self, state):
        """Return a list of the allowable moves at this point."""
        if self.terminal_test(state):
            return []
        else:
            return self.moves