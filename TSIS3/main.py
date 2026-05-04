import pygame  # imports pygame library for graphics, window, fonts, and events
import sys  # imports sys library to exit the program
from racer import run_game  # imports the main game function from racer.py
from ui import draw_button, username_screen, leaderboard_screen, settings_screen, game_over_screen  # imports UI-related functions
from persistence import load_settings, save_settings, save_score  # imports functions for saving/loading data

pygame.init()  # initializes all pygame modules (window, events, fonts, etc.)

WIDTH = 700  # width of the game window
HEIGHT = 500  # height of the game window

screen = pygame.display.set_mode((WIDTH, HEIGHT))  # creates the main game window
pygame.display.set_caption("Racer PRO")  # sets the window title

font_big = pygame.font.SysFont("Verdana", 42)  # large font for titles
font = pygame.font.SysFont("Verdana", 26)  # medium font for buttons
font_small = pygame.font.SysFont("Verdana", 18)  # small font for secondary text


def main_menu():  # function that controls the main menu screen
    settings = load_settings()  # loads saved settings from settings.json

    play_button = pygame.Rect(220, 110, 260, 55)  # rectangle for Play button
    leaderboard_button = pygame.Rect(220, 190, 260, 55)  # rectangle for Leaderboard button
    settings_button = pygame.Rect(220, 270, 260, 55)  # rectangle for Settings button
    quit_button = pygame.Rect(220, 350, 260, 55)  # rectangle for Quit button

    while True:  # infinite loop for menu
        screen.fill((20, 20, 20))  # fills screen with dark background color

        title = font_big.render("Racer PRO", True, (255, 255, 255))  # renders title text
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 35))  # draws title centered at top

        draw_button(screen, "Play", play_button, font)  # draws Play button
        draw_button(screen, "Leaderboard", leaderboard_button, font)  # draws Leaderboard button
        draw_button(screen, "Settings", settings_button, font)  # draws Settings button
        draw_button(screen, "Quit", quit_button, font)  # draws Quit button

        pygame.display.update()  # updates screen with all drawn elements

        for event in pygame.event.get():  # processes all events (mouse, keyboard, etc.)
            if event.type == pygame.QUIT:  # if user closes window
                save_settings(settings)  # saves current settings to file
                pygame.quit()  # closes pygame
                sys.exit()  # exits program

            if event.type == pygame.MOUSEBUTTONDOWN:  # if mouse is clicked
                if play_button.collidepoint(event.pos):  # if Play button is clicked
                    username = username_screen(screen, font_big, font, font_small)  # opens username input screen

                    if username:  # if user entered a valid name
                        while True:  # loop for replaying the game
                            result = run_game(screen, username, settings)  # runs the main game and gets result
                            save_score(result)  # saves result to leaderboard file

                            action = game_over_screen(screen, font_big, font, result)  # shows game over screen

                            if action == "menu":  # if user chooses to go back to menu
                                break  # break inner loop and return to main menu

                elif leaderboard_button.collidepoint(event.pos):  # if Leaderboard button is clicked
                    leaderboard_screen(screen, font_big, font, font_small)  # opens leaderboard screen

                elif settings_button.collidepoint(event.pos):  # if Settings button is clicked
                    settings_screen(screen, font_big, font, settings)  # opens settings screen

                elif quit_button.collidepoint(event.pos):  # if Quit button is clicked
                    save_settings(settings)  # saves settings before exit
                    pygame.quit()  # closes pygame
                    sys.exit()  # exits program


main_menu()  # starts the program by calling main menu