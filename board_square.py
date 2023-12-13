import pygame


from typing import Union


class Board_Square:
    instance_count = 0

    def __init__(self, row, col, symbol):
        self.row = row
        self.col = col
        self.selected = False
        self.symbol = symbol

