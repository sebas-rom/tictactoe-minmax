import pygame

#from const import *

from confs import B_COLS, B_ROWS
from board_square import Board_Square
import numpy as np

from typing import Union


class Board:
    instance_count = 0

    def __init__(self, window):
        self.window = window
        self.board_squares = None
        self.board_squares_numpy = None
        self.ai_algo_board = None
    def build_board(self):
        from confs import BOARD_X_OFFSET, img_white_square, SQUARE_SIZE, BOARD_Y_OFFSET, SQUARE_SIZE
        self.board_squares = [[Board_Square(row, col, 0) for col in range(B_COLS)] for row in range(B_ROWS)]
        self.board_squares_numpy = np.array(self.board_squares)
        for row, rows_square_objs in enumerate(self.board_squares):
            for col, cols_square_obj in enumerate(rows_square_objs):
                self.window.blit(img_white_square, (BOARD_X_OFFSET + col * SQUARE_SIZE, BOARD_Y_OFFSET + row * SQUARE_SIZE))