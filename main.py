import sys
import time
import random

from collections import namedtuple

import pygame
from confs import SQUARE_SIZE, BOARD_Y_OFFSET, BOARD_X_OFFSET, img_white_square
from board import Board
from confs import WHITE_COLOR, B_ROWS, B_COLS, BOARD_X_OFFSET, BOARD_Y_OFFSET, PLAYER_ONE, PLAYER_TWO, window, TERMINAL_STATE
from game_management import Game_mngmt
from ai_algorithms import minmax_decision, actions, minmax_decision_pruning
import copy

def draw_button(rect_position, text, action_text, action):
    font = pygame.font.Font(None, 36)
    button_width, button_height = 200, 50
    space_between_buttons = 10

    play_button = pygame.Rect(rect_position[0], rect_position[1], button_width, button_height)
    pygame.draw.rect(window, (0, 0, 0), play_button)

    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(rect_position[0] + button_width // 2, rect_position[1] + button_height // 2))
    window.blit(text_surface, text_rect)

    pygame.display.flip()

    return play_button

def draw_interface():
    button_position = (window.get_width() // 2 - 100, window.get_height() // 2 - 75)

    play_first_button = draw_button(button_position, "Play First", "Play First", None)
    play_second_button = draw_button(
        (button_position[0], button_position[1] + 15 + 40),
        "Play Second", "Play Second", None
    )

    return play_first_button, play_second_button

def draw_second_interface():
    button_position = (window.get_width() // 2 - 100, window.get_height() // 2 - 75)

    play_minmax_button = draw_button(button_position, "Play MinMax", "Play MinMax", None)
    play_alpha_beta_button = draw_button(
        (button_position[0], button_position[1] + 15 + 40),
        "Play Alpha Beta", "Play Alpha Beta", None
    )

    return play_minmax_button, play_alpha_beta_button

def main():
    play_first_button, play_second_button = draw_interface()

    # Wait for user input to determine who plays first
    waiting_for_input = True
    my_turn = True  # Default value, can be adjusted based on user input
    is_player_two_min = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if play_first_button.collidepoint(mouse_x, mouse_y):
                    waiting_for_input = False
                    my_turn = True
                    is_player_two_min = True
                elif play_second_button.collidepoint(mouse_x, mouse_y):
                    waiting_for_input = False
                    my_turn = False
                    is_player_two_min = False

    # Remove buttons after choice is made
    pygame.draw.rect(window, (255, 255, 255), play_first_button)
    pygame.draw.rect(window, (255, 255, 255), play_second_button)
    pygame.display.flip()

    # Display new set of buttons
    play_minmax_button, play_alpha_beta_button = draw_second_interface()

    # Wait for user input to determine which algorithm to play
    waiting_for_input = True
    is_minmax = True  # Default value, can be adjusted based on user input
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if play_minmax_button.collidepoint(mouse_x, mouse_y):
                    waiting_for_input = False
                    is_minmax = True
                elif play_alpha_beta_button.collidepoint(mouse_x, mouse_y):
                    waiting_for_input = False
                    is_minmax = False

    # Remove second set of buttons after choice is made
    pygame.draw.rect(window, (255, 255, 255), play_minmax_button)
    pygame.draw.rect(window, (255, 255, 255), play_alpha_beta_button)
    pygame.display.flip()

    board = Board(window)
    board.build_board()
    game_mngmt = Game_mngmt(board)
    game_over = False
    cell_col = None
    cell_row = None
    pygame.display.flip()
    pygame.display.update()
    print("is_minmax: ", is_minmax)
    print("is_player_two_min: ", is_player_two_min)
    ai_thinking = False  # Add a flag to track whether AI is thinking

    # If the AI is starting, make a random move
    if not my_turn:
        ai_thinking = True
        pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)

        # Choose a random move
        random_col = random.randint(0, B_COLS - 1)
        random_row = random.randint(0, B_ROWS - 1)

        # Make the move
        game_mngmt.mark(random_row, random_col, window, game_mngmt.board.board_squares)

        pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
        ai_thinking = False
        my_turn = not my_turn  # Toggle turn

    check_terminal(game_mngmt)

    # The game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            # Player's turn
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over and my_turn and not ai_thinking:
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
                check_terminal(game_mngmt)

            # AI's turn
            elif not game_over and not my_turn and not ai_thinking:
                # Add the "AI thinking" text on top of the game
                font = pygame.font.Font(None, 36)
                ai_thinking_text = font.render("AI thinking", True, (255, 0, 0))
                window.blit(ai_thinking_text, (BOARD_X_OFFSET, BOARD_Y_OFFSET - 40))

                pygame.display.flip()
                pygame.display.update()

                # Block player's mouse events during AI's move
                pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
                ai_thinking = True

                # Choose algorithm
                if is_minmax:
                    x, y = minmax_decision(game_mngmt.board.board_squares, is_player_two_min)
                else:
                    x, y = minmax_decision_pruning(game_mngmt.board.board_squares, is_player_two_min)

                # Move
                game_mngmt.mark(x, y, window, game_mngmt.board.board_squares)

                # Allow player's mouse events after AI's move
                pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
                ai_thinking = False
                my_turn = not my_turn  # Toggle turn

                # Remove the "AI thinking" text after AI's move
                window.fill((255, 255, 255), (BOARD_X_OFFSET, BOARD_Y_OFFSET - 40, 200, 40))

                # Clear the event queue to prevent processing old events
                pygame.event.clear()

                check_terminal(game_mngmt)

def check_terminal(game_mngmt):
    pygame.display.flip()
    pygame.display.update()
    status = game_mngmt.check_gamestatus(game_mngmt.board.board_squares)
    terminal_statuses = [TERMINAL_STATE.MAX_WON, TERMINAL_STATE.MIN_WON, TERMINAL_STATE.TIE_GAME]

    if status in terminal_statuses:
        font = pygame.font.Font(None, 50)
        if status == TERMINAL_STATE.MAX_WON:
            message = "Player One Wins!"
        elif status == TERMINAL_STATE.MIN_WON:
            message = "Player Two Wins!"
        else:
            message = "It's a Tie!"

        text = font.render(message, True, (0, 0, 255))
        text_rect = text.get_rect(center=(window.get_width() // 2, window.get_height() // 4))
        window.blit(text, text_rect)
        pygame.display.flip()

        # Add "Play Again" and "Quit Game" buttons
        play_again_button = draw_button((window.get_width() // 2 - 100, window.get_height() - 140), "Play Again", "Play Again", None)
        quit_game_button = draw_button((window.get_width() // 2 - 100, window.get_height() - 80), "Quit Game", "Quit Game", None)

        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if play_again_button.collidepoint(mouse_x, mouse_y):
                        # Erase all contents on the screen
                        window.fill((255, 255, 255))
                        # Restart the game
                        main()
                    elif quit_game_button.collidepoint(mouse_x, mouse_y):
                        sys.exit()

if __name__ == '__main__':
    main()