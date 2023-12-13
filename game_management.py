from confs import *
from board_square import *
from collections import namedtuple
GameState = namedtuple('GameState', 'to_move, utility, board, moves')

class Game_mngmt:

    def __init__(self, board):
        self.current_player = PLAYER_ONE
        self.board = board
        self.moves = None
        self.reset_moves()

    def set_moves(self,moves):
        self.moves = moves

    def set_curr_player(self, player):
        self.current_player = player

    def reset_moves(self, state=[]):
        board = {}
        moves = []
        for row_number, all_row in enumerate(self.board.board_squares):
            for col_number, board_square  in enumerate(all_row):
                if board_square.symbol == 0:
                    moves.append((col_number+1, row_number+1))
                if board_square.symbol == 1:
                    board[(col_number + 1, row_number + 1)] = 'X'
                if board_square.symbol == 2:
                    board[(col_number + 1, row_number + 1)] = 'O'

        self.set_moves(moves)
        if state != []:
            state = GameState(to_move=state.to_move, utility=state.utility, board=board, moves=moves)
        return state

    def check_gamestatus(self, cells):
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
                print("DIAGONAL: PLAYER_ONE WON")
                return TERMINAL_STATE.MAX_WON

            if diag_count_pl2 == B_ROWS:
                print("DIAGONAL: PLAYER_TWO WON")
                return TERMINAL_STATE.MIN_WON

            for col in range(B_COLS):
                if cells[row][col].symbol == 1:
                    cols_count_pl1 += 1
                    board_filled_count += 1
                elif cells[row][col].symbol == 2:
                    cols_count_pl2 += 1
                    board_filled_count += 1

                if cols_count_pl1 == B_COLS:
                    print("ROW", row, "WAS FILLED BY PLAYER_ONE - PLAYER_ONE_WON")
                    return TERMINAL_STATE.MAX_WON

                if cols_count_pl2 == B_COLS:
                    print("ROW", row, "WAS FILLED BY PLAYER_TWO - PLAYER_TWO_WON")
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
                            print("COL", col, "FILLED BY PLAYER_ONE - PLAYER_ONE_WON")
                            return TERMINAL_STATE.MAX_WON

                        if rows_count_pl2 == B_ROWS:
                            print("COL", col, "FILLED BY PLAYER_TWO - PLAYER_TWO_WON")
                            return TERMINAL_STATE.MIN_WON

        if board_filled_count == B_ROWS * B_ROWS:
            print("TIE")
            return TERMINAL_STATE.TIE_GAME
        else:
            return TERMINAL_STATE.NOT_TERMINAL

    def mark(self, row, col, window, cells, algo = False):

        if algo:
            cells[row][col].symbol = 1
            x = BOARD_X_OFFSET + col * SQUARE_SIZE + img_white_square.get_rect().centerx - img_cross.get_rect().width // 2
            y = BOARD_Y_OFFSET + row * SQUARE_SIZE + img_white_square.get_rect().centery - img_cross.get_rect().height // 2
            window.blit(img_cross, (x, y))
            self.current_player = PLAYER_TWO
            return

        if self.current_player == PLAYER_ONE and cells[row][col].symbol == 0:
            x = BOARD_X_OFFSET + col * SQUARE_SIZE + img_white_square.get_rect().centerx - img_cross.get_rect().width //2
            y = BOARD_Y_OFFSET + row * SQUARE_SIZE + img_white_square.get_rect().centery - img_cross.get_rect().height // 2
            cells[row][col].symbol = 1
            window.blit(img_cross, (x, y))

            self.current_player = PLAYER_TWO
        elif cells[row][col].symbol == 0:
            x = BOARD_X_OFFSET + col * SQUARE_SIZE + img_white_square.get_rect().centerx - img_cross.get_rect().width // 2
            y = BOARD_Y_OFFSET + row * SQUARE_SIZE + img_white_square.get_rect().centery - img_cross.get_rect().height // 2
            cells[row][col].symbol = 2
            window.blit(img_nought, (x, y))
            self.current_player = PLAYER_ONE

    def set_with_algorithm(self, move, copy_of_board):
        col,row = move
        player = self.current_player
        if player == PLAYER_ONE:
            copy_of_board[row][col].symbol = 1
            self.current_player = PLAYER_TWO
        else:
            copy_of_board[row][col].symbol = 2
            self.current_player = PLAYER_ONE
        return   copy_of_board

