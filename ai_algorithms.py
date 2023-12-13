"""Games or Adversarial Search (Chapter 5)"""

import copy
import itertools
import random
from collections import namedtuple

import numpy as np



GameState = namedtuple('GameState', 'to_move, utility, board, moves')
StochasticGameState = namedtuple('StochasticGameState', 'to_move, utility, board, moves, chance')

class Game:
    pass

from game_management import *
class TicTacToe(Game):
  pass



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



