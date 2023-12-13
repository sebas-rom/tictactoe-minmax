"""Games or Adversarial Search (Chapter 5)"""

import copy
import itertools
import random
from collections import namedtuple
import game_management
from confs import *
import numpy as np



GameState = namedtuple('GameState', 'to_move, utility, board, moves')
def minmax_decision(state):
    """
    Returns the best move for the AI player using the minimax algorithm.
    """
    _, move = max_value(state)
    return move


def max_value(state):
    """
    Maximize the utility value for the AI player.
    """
    if terminal_test(state):
        return utility(state), None

    max_utility = -9999999
    best_move = None

    for action in actions(state):
        next_state = result(state, action)
        min_val, _ = min_value(next_state)

        if min_val > max_utility:
            max_utility = min_val
            best_move = action

    return max_utility, best_move


def min_value(state):
    """
    Minimize the utility value for the opponent player.
    """
    if terminal_test(state):
        return utility(state), None

    min_utility = 9999999
    best_move = None

    for action in actions(state):
        next_state = result(state, action)
        max_val, _ = max_value(next_state)

        if max_val < min_utility:
            min_utility = max_val
            best_move = action

    return min_utility, best_move


def terminal_test(state):
    """
    Check if the current state is a terminal state.
    """
    # Implement your logic to determine if the game is in a terminal state
    # This will depend on the structure of your GameState and TERMINAL_STATE enums.
    # You can compare the state to TERMINAL_STATE values to check if the game has ended.
    return state is not None and state in [TERMINAL_STATE.MAX_WON, TERMINAL_STATE.MIN_WON, TERMINAL_STATE.TIE_GAME]


def utility(state):
    """
    Assign utility values to terminal states.
    """
    # Implement your logic to assign utility values based on the outcome of the game.
    # You can use the TERMINAL_STATE enum to determine the outcome.
    if state == TERMINAL_STATE.MAX_WON:
        return MAX_WON_UTIL
    elif state == TERMINAL_STATE.MIN_WON:
        return MIN_WON_UTIL
    elif state == TERMINAL_STATE.TIE_GAME:
        return TIE_UTIL
    else:
        # Non-terminal state; return a default value
        return 0


def actions(state):
    """
    Generate possible actions for the current state.
    """
    # based on a state, return a list of possible actions
    # each action is a tuple of (row, col)
    actions = []
    for row in state:
        i=state.index(row)
        for col in row:
            j=row.index(col)
            if col.symbol == 0:
                actions.append((i,j))
    
    print (actions)
    return actions
    

def result(state, action):
    """
    Apply the action to the current state and return the new state.
    """
    # Implement your logic to apply the action to the current state and return the new state.
    # This will depend on the structure of your GameState.
    state = copy.deepcopy(state)
    state[action[0]][action[1]].symbol = 2
    
    
    return state  # Placeholder; replace with actual implementation

        
        
   