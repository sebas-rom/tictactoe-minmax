"""Games or Adversarial Search (Chapter 5)"""

import copy
import itertools
import random
from collections import namedtuple

import numpy as np
from game_management import Game_mngmt
from board import Board
from confs import window,TERMINAL_STATE, B_ROWS, B_COLS, PLAYER_ONE, PLAYER_TWO
from board_square import Board_Square

def minmax_decision(state):
    """
    Returns the best move for the AI player using the minimax algorithm.
    """
    _, move = min_value(state)
    return move

def max_value(state):
    """
    Maximize the utility value for the AI player.
    """
    # print("max_value loop")
    if terminal_test(state):
        # print("is terminal, value:",utility(state))
        return utility(state), None
    
    max_utility = -9999999
    best_move = None

    for action in actions(state):
        next_state = result(state, action)
        min_val, _ = min_value(next_state)

        if min_val > max_utility:
            # print("max choosing action: ",action," value:",min_val)
            max_utility = min_val
            best_move = action

    return max_utility, best_move

def min_value(state):
    """
    Minimize the utility value for the opponent player.
    """
    # print("____min_value loop")
    if terminal_test(state):
        # print("is terminal, value:",utility(state))
        return utility(state), None

    min_utility = 9999999
    best_move = None

    for action in actions(state):
        # print("action: ",action)
        next_state = result(state, action)
        max_val, _ = max_value(next_state)

        if max_val < min_utility:
            #print("min choosing action: ",action," value:",max_val)
            min_utility = max_val
            best_move = action

    return min_utility, best_move

def terminal_test(state):
    """
    Check if the current state is a terminal state.
    """
     # Create a shallow copy of the window
    status = check_gamestatus(state)
    isTerminal = False
    if status.value != 4:
        isTerminal = True
    return isTerminal

def utility(state):
    """
    Assign utility values to terminal states.
    """
    
    status = check_gamestatus(state)
    if(status==TERMINAL_STATE.TIE_GAME):
        return 0
    elif(status==TERMINAL_STATE.MAX_WON):
        return 1
    elif(status==TERMINAL_STATE.MIN_WON):
        return -1

def actions(state):
    """
    Generate possible actions for the current state.
    """
    possible_actions = []

    # Iterate through each row and column of the board
    for row in range(B_ROWS):
        for col in range(B_COLS):
            # Check if the square is empty (0 indicates an empty square)
            if state[row][col].symbol == 0:
                # If the square is empty, add it to the list of possible actions
                possible_actions.append((row, col))
    return possible_actions
    
def result(state, action):
    """
    Apply the action to the current state and return the new state.
    """
    state_copy = copy.deepcopy(state)
    # Set the current player to the player who will play next
    current_player = who_plays_next(state_copy)
    # Mark the action on the copied state
    mark(action[0], action[1], state_copy, current_player)
    # print("result:  from action: ",action)
    # print_board(state_copy)
    return state_copy

def who_plays_next(cells):
    player_one_count = 0
    player_two_count = 0
    for row in cells:
        for cell in row:
            if cell.symbol == 1:
                player_one_count += 1
            elif cell.symbol == 2:
                player_two_count += 1
    if player_one_count > player_two_count:
        return PLAYER_TWO
    else:
        return PLAYER_ONE
def print_board(cells, print_XO=True):
    for row in cells:
        for cell in row:
            if print_XO:
                if cell.symbol == 0:
                    print('-', end=" ")
                elif cell.symbol == 1:
                    print('X', end=" ")
                elif cell.symbol == 2:
                    print('O', end=" ")
            else:
                print(cell.symbol, end=" ")
        print()


def test_minmax_decision():
    # board_squares_data = [
    #     [2, 2, 1],
    #     [1, 0, 2],
    #     [0, 0, 1]
    # ]
    # board_squares_data = [
    #     [1, 2, 2],
    #     [0, 1, 0],
    #     [0, 1, 2]
    # ]
    board_squares_data = [
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 0]
    ]
    
    initial_state = [
        [Board_Square(row, col, value) for col, value in enumerate(row_data)] 
        for row, row_data in enumerate(board_squares_data)
    ]
    # print("Initial State:")
    # print_board(initial_state)
    # print("Starting...")

    ai_move = minmax_decision(initial_state)

    print("\nAI Move:")
    print(ai_move)
def check_gamestatus(cells):
        diag_count_pl1 = 0
        diag_count_pl2 = 0
        board_filled_count = 0
        for row in range(B_ROWS):
            cols_count_pl1 = 0
            cols_count_pl2 = 0

            if row == 1:
                if cells[row][row].symbol == 1  and  cells[row+1][row+1].symbol == 1 and \
                        cells[row-1][row-1].symbol == 1:
                    diag_count_pl1 = 3
                if cells[row][row].symbol == 2 and cells[row + 1][row + 1].symbol == 2 and \
                        cells[row - 1][row - 1].symbol == 2:
                    diag_count_pl2 = 3

                if cells[row][row].symbol == 1 and cells[row - 1][row + 1].symbol == 1 and \
                        cells[row + 1][row - 1].symbol == 1:
                    diag_count_pl1 = 3
                if cells[row][row].symbol == 2 and cells[row - 1][row + 1].symbol == 2 and \
                        cells[row + 1][row - 1].symbol == 2:
                    diag_count_pl2 = 3

            if diag_count_pl1 == B_ROWS:
                return TERMINAL_STATE.MAX_WON

            if diag_count_pl2 == B_ROWS:
                return TERMINAL_STATE.MIN_WON

            for col in range(B_COLS):
                if cells[row][col].symbol == 1:
                    cols_count_pl1 += 1
                    board_filled_count += 1
                elif cells[row][col].symbol == 2:
                    cols_count_pl2 += 1
                    board_filled_count += 1

                if cols_count_pl1 == B_COLS:
                    return TERMINAL_STATE.MAX_WON

                if cols_count_pl2 == B_COLS:
                    return TERMINAL_STATE.MIN_WON

                if row == 0:
                    rows_count_pl1 = 0
                    rows_count_pl2 = 0
                    for row_test in range(B_ROWS):
                        if cells[row_test][col].symbol == 1:
                            rows_count_pl1 += 1
                        elif cells[row_test][col].symbol == 2:
                            rows_count_pl2 += 1

                        if rows_count_pl1 == B_ROWS:
                            return TERMINAL_STATE.MAX_WON

                        if rows_count_pl2 == B_ROWS:
                            return TERMINAL_STATE.MIN_WON

        if board_filled_count == B_ROWS * B_ROWS:
            return TERMINAL_STATE.TIE_GAME
        else:
            return TERMINAL_STATE.NOT_TERMINAL

def mark(row, col, cells, current_player):
        if current_player == PLAYER_ONE and cells[row][col].symbol == 0:
            cells[row][col].symbol = 1
            current_player = PLAYER_TWO
        elif cells[row][col].symbol == 0:
            cells[row][col].symbol = 2
            current_player = PLAYER_ONE

if __name__ == "__main__":
    test_minmax_decision()       
   