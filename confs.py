import pygame

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

img_nought = pygame.image.load("icons/oo.jpg")
img_cross = pygame.image.load("icons/xx.jpg")
img_white_square = pygame.image.load("icons/smaller_black_edges.gif")

SQUARE_SIZE = None

B_ROWS = 3
B_COLS = 3
WHITE_COLOR = (255, 255, 255)

pygame.init()
pygame.display.init()
flags = pygame.DOUBLEBUF | pygame.HWSURFACE
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), flags)
window.fill(WHITE_COLOR)
img_nought = img_nought.convert(window)
img_cross = img_cross.convert(window)
img_white_square = img_white_square.convert(window)
pygame.display.flip()
pygame.display.update()

SQUARE_SIZE = img_white_square.get_width()
BOARD_WIDTH = SQUARE_SIZE * B_COLS
BOARD_HEIGHT = SQUARE_SIZE * B_ROWS

BOARD_X_OFFSET = WINDOW_WIDTH // 2 - BOARD_WIDTH // 2
BOARD_Y_OFFSET = WINDOW_HEIGHT // 2 - BOARD_HEIGHT // 2 - 5


# class IconMngmt:
#     def __init__(self):
#         self.img_nought = pygame.image.load("icons/oo.jpg")
#         self.img_cross = pygame.image.load("icons/xx.jpg")
#         self.img_white_square = pygame.image.load("icons/smaller_black_edges.gif")
#
#     def process_icons(self, window):
#         self.img_nought = self.img_nought.convert(window)
#         self.img_cross = self.img_cross.convert(window)
#         self.img_white_square = self.img_white_square.convert(window)




# BOARD_WIDTH = None
# BOARD_HEIGHT = None
#
# BOARD_X_OFFSET = None
# BOARD_Y_OFFSET = None
#
# def init_images(img_mngmt):
#     global img_nought
#     global img_cross
#     global img_white_square
#     global SQUARE_SIZE, BOARD_WIDTH, BOARD_HEIGHT
#     global BOARD_X_OFFSET, BOARD_Y_OFFSET
#
#     img_nought = img_mngmt.img_nought
#     img_cross = img_mngmt.img_cross
#     img_white_square = img_mngmt.img_white_square
#     SQUARE_SIZE = img_white_square.get_width()
#     BOARD_WIDTH = SQUARE_SIZE * B_COLS
#     BOARD_HEIGHT = SQUARE_SIZE * B_ROWS
#
#     BOARD_X_OFFSET = WINDOW_WIDTH // 2 - BOARD_WIDTH // 2
#     BOARD_Y_OFFSET = WINDOW_HEIGHT // 2 - BOARD_HEIGHT // 2 - 5








PLAYER_ONE = 1
PLAYER_TWO = 2

PLAYER_ONE_WON = "Player 1 won."
PLAYER_TWO_WON = "Player 2 won."
TIE_GAME = "Tie game."

MAX_WON_UTIL = 1
MIN_WON_UTIL = -1
TIE_UTIL = 0


from enum import Enum

# class syntax
class TERMINAL_STATE(Enum):
    MAX_WON = 1
    MIN_WON = 2
    TIE_GAME = 3
    NOT_TERMINAL = 4
    TERMINAL = 5



