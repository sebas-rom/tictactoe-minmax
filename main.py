from collections import namedtuple

import pygame
from confs import SQUARE_SIZE, BOARD_Y_OFFSET, BOARD_X_OFFSET, img_white_square
from board import Board
from confs import WHITE_COLOR, B_ROWS, B_COLS, BOARD_X_OFFSET, \
    BOARD_Y_OFFSET, PLAYER_ONE, PLAYER_TWO, window, TERMINAL_STATE
import copy

from game_management import Game_mngmt
import sys
from ai_algorithms import minmax_decision,actions,minmax_decision_pruning
import time
GameState = namedtuple('GameState', 'to_move, utility, board, moves')
def main():


    board = Board(window)
    board.build_board()
    game_mngmt = Game_mngmt(board)
    game_over = False
    cell_col = None
    cell_row = None
    pygame.display.flip()
    pygame.display.update()
    my_turn = True  # Initialize to True for the first move

    while True:


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            # Player's turn
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over and my_turn:
                # mark the appropriate tile
                # get the position of the mouse
                mouse_x, mouse_y = pygame.mouse.get_pos()

                for col in range(B_COLS):
                    if mouse_x <= BOARD_X_OFFSET + col * SQUARE_SIZE + SQUARE_SIZE:
                        cell_col = col
                        break

                for row in range(B_ROWS):
                    if mouse_y <= BOARD_Y_OFFSET + row * SQUARE_SIZE + SQUARE_SIZE:
                        cell_row = row
                        break

                game_mngmt.mark(cell_row, cell_col, window, game_mngmt.board.board_squares)
                actions(game_mngmt.board.board_squares)
                my_turn = not my_turn  # Toggle turn
                pygame.display.flip()
                pygame.display.update()
                status = game_mngmt.check_gamestatus(game_mngmt.board.board_squares)
                check_terminal(status)
            
            # #AI's turn
            elif not game_over and not my_turn:
                move= minmax_decision_pruning(game_mngmt.board.board_squares)
                x,y=move
                game_mngmt.mark(x, y, window, game_mngmt.board.board_squares)

                my_turn = not my_turn  # Toggle turn

                pygame.display.flip()
                pygame.display.update()
                status = game_mngmt.check_gamestatus(game_mngmt.board.board_squares)
                check_terminal(status)

def check_terminal(status):
    terminal_statuses = [TERMINAL_STATE.MAX_WON, TERMINAL_STATE.MIN_WON, TERMINAL_STATE.TIE_GAME]

    if status in terminal_statuses:
        font = pygame.font.Font(None, 50)
        if status == TERMINAL_STATE.MAX_WON:
            message = "Player One Wins!"
        elif status == TERMINAL_STATE.MIN_WON:
            message = "Player Two Wins!"
        else:
            message = "It's a Tie!"

        text = font.render(message, True, (0,0,255))
        text_rect = text.get_rect(center=(window.get_width() // 2, window.get_height() // 4))

        window.blit(text, text_rect)
        pygame.display.flip()
        time.sleep(4)
        sys.exit()




if __name__ == '__main__':
    main()