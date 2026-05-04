import pygame  # pygame library is used for creating window, drawing graphics, handling input
import sys     # sys is used to completely exit the program

from game import run_game  # this function runs the main snake gameplay
from db import get_top10   # this function loads leaderboard data from PostgreSQL
from config import load_settings, save_settings  # these handle reading and writing settings.json

pygame.init()  # initialize all pygame modules (window, fonts, etc.)

WIDTH = 600   # width of the game window
HEIGHT = 400  # height of the game window

# create the window with given size
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# set the title at the top of the window
pygame.display.set_caption("Snake PRO")

# create fonts that will be reused in different screens
font_big = pygame.font.SysFont("Verdana", 40)   # used for titles like "Game Over"
font = pygame.font.SysFont("Verdana", 26)       # used for buttons and main text
font_small = pygame.font.SysFont("Verdana", 18) # used for smaller text like leaderboard rows


def draw_button(text, rect):
    # this function draws a button with text centered inside

    # draw button background (dark gray)
    pygame.draw.rect(screen, (60, 60, 60), rect)

    # draw white border around button
    pygame.draw.rect(screen, (255, 255, 255), rect, 2)

    # render text into an image
    label = font.render(text, True, (255, 255, 255))

    # draw text so that it is centered inside the rectangle
    screen.blit(label, (
        rect.centerx - label.get_width() // 2,
        rect.centery - label.get_height() // 2
    ))


def username_screen():
    # this screen asks the player to enter their name before starting the game

    name = ""  # empty string that will store typed characters

    while True:  # loop runs until player presses Enter
        screen.fill((20, 20, 20))  # fill background with dark color

        # draw title text
        title = font_big.render("Enter Name", True, (255, 255, 255))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))

        # create rectangle for input field
        box = pygame.Rect(150, 180, 300, 50)

        # draw input box border
        pygame.draw.rect(screen, (255, 255, 255), box, 2)

        # render current typed name
        text = font.render(name, True, (255, 255, 255))

        # draw text inside input box with small offset
        screen.blit(text, (box.x + 10, box.y + 10))

        # draw hint text
        hint = font_small.render("Press Enter to start", True, (255, 255, 255))
        screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, 250))

        pygame.display.update()  # update everything on screen

        for e in pygame.event.get():  # check all events (keyboard, mouse, close)
            if e.type == pygame.QUIT:  # if user clicks X
                pygame.quit()
                sys.exit()

            if e.type == pygame.KEYDOWN:  # if a key is pressed
                if e.key == pygame.K_RETURN and name.strip() != "":
                    return name.strip()  # return entered name and exit screen

                elif e.key == pygame.K_BACKSPACE:
                    name = name[:-1]  # remove last character

                else:
                    name += e.unicode  # add typed character to string


def leaderboard_screen():
    # this screen displays top 10 scores from database

    back_button = pygame.Rect(200, 330, 200, 50)  # button to go back

    while True:
        screen.fill((0, 0, 50))  # dark blue background

        # draw title
        title = font_big.render("Leaderboard", True, (255, 255, 255))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 30))

        data = get_top10()  # get list of top scores from database

        y = 100  # starting vertical position for text

        if not data:  # if no scores exist
            txt = font.render("No scores yet", True, (255, 255, 255))
            screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, 200))
        else:
            # loop through all results and draw them
            for i, row in enumerate(data):
                # row[0] = username, row[1] = score, row[2] = level
                line = f"{i+1}. {row[0]} | Score: {row[1]} | Lvl: {row[2]}"
                txt = font_small.render(line, True, (255, 255, 255))
                screen.blit(txt, (40, y))
                y += 25  # move down for next line

        draw_button("Back", back_button)

        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(e.pos):
                    return  # exit leaderboard screen


def color_picker_screen(settings):
    # this screen allows player to choose snake color

    # list of available colors (name + RGB)
    colors = [
        ("green", [170, 200, 50]),
        ("red", [255, 80, 80]),
        ("blue", [80, 120, 255]),
        ("lightgreen", [80, 255, 120]),
        ("yellow", [255, 255, 0])
    ]

    # create clickable rectangles for each color
    rects = [pygame.Rect(80 + i * 90, 180, 60, 60) for i in range(len(colors))]

    back_btn = pygame.Rect(200, 300, 200, 50)

    while True:
        screen.fill((20, 20, 20))

        title = font_big.render("Choose Color", True, (255, 255, 255))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))

        # draw color squares
        for i, rect in enumerate(rects):
            pygame.draw.rect(screen, colors[i][1], rect)

            # if this color is currently selected, draw border
            if colors[i][1] == settings["snake_color"]:
                pygame.draw.rect(screen, (255, 255, 255), rect, 3)

        draw_button("Back", back_btn)

        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type == pygame.MOUSEBUTTONDOWN:
                # check if any color box was clicked
                for i, rect in enumerate(rects):
                    if rect.collidepoint(e.pos):
                        settings["snake_color"] = colors[i][1]

                # go back
                if back_btn.collidepoint(e.pos):
                    return


def settings_screen(settings):
    # this screen allows changing game settings

    sound_btn = pygame.Rect(180, 120, 240, 50)
    grid_btn = pygame.Rect(180, 190, 240, 50)
    color_btn = pygame.Rect(180, 260, 240, 50)
    back_btn = pygame.Rect(180, 330, 240, 50)

    while True:
        screen.fill((30, 20, 20))

        title = font_big.render("Settings", True, (255, 255, 255))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 40))

        # show current settings values
        draw_button(f"Sound: {'ON' if settings['sound'] else 'OFF'}", sound_btn)
        draw_button(f"Grid: {'ON' if settings['grid'] else 'OFF'}", grid_btn)
        draw_button("Snake Color", color_btn)
        draw_button("Back", back_btn)

        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                save_settings(settings)
                pygame.quit()
                sys.exit()

            if e.type == pygame.MOUSEBUTTONDOWN:
                if sound_btn.collidepoint(e.pos):
                    settings["sound"] = not settings["sound"]  # toggle sound

                elif grid_btn.collidepoint(e.pos):
                    settings["grid"] = not settings["grid"]  # toggle grid

                elif color_btn.collidepoint(e.pos):
                    color_picker_screen(settings)  # open color selection

                elif back_btn.collidepoint(e.pos):
                    save_settings(settings)  # save before exit
                    return


def game_over_screen(result):
    # screen shown after player loses

    retry_btn = pygame.Rect(180, 250, 240, 50)
    menu_btn = pygame.Rect(180, 320, 240, 50)

    while True:
        screen.fill((120, 0, 0))  # red background

        title = font_big.render("GAME OVER", True, (255, 255, 255))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

        # display game results
        screen.blit(font.render(f"Score: {result['score']}", True, (255, 255, 255)), (200, 130))
        screen.blit(font.render(f"Level: {result['level']}", True, (255, 255, 255)), (200, 160))
        screen.blit(font.render(f"Best: {result['best']}", True, (255, 255, 255)), (200, 190))

        draw_button("Retry", retry_btn)
        draw_button("Menu", menu_btn)

        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type == pygame.MOUSEBUTTONDOWN:
                if retry_btn.collidepoint(e.pos):
                    return "retry"  # restart game

                if menu_btn.collidepoint(e.pos):
                    return "menu"  # return to menu


def main_menu():
    # this is the first screen that appears when program starts

    settings = load_settings()  # load saved settings

    play_btn = pygame.Rect(180, 100, 240, 50)
    leaderboard_btn = pygame.Rect(180, 170, 240, 50)
    settings_btn = pygame.Rect(180, 240, 240, 50)
    quit_btn = pygame.Rect(180, 310, 240, 50)

    while True:
        screen.fill((20, 20, 20))

        title = font_big.render("Snake PRO", True, (255, 255, 255))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 30))

        draw_button("Play", play_btn)
        draw_button("Leaderboard", leaderboard_btn)
        draw_button("Settings", settings_btn)
        draw_button("Quit", quit_btn)

        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                save_settings(settings)
                pygame.quit()
                sys.exit()

            if e.type == pygame.MOUSEBUTTONDOWN:
                if play_btn.collidepoint(e.pos):
                    name = username_screen()

                    while True:
                        result = run_game(screen, name, settings)
                        action = game_over_screen(result)

                        if action == "menu":
                            break

                elif leaderboard_btn.collidepoint(e.pos):
                    leaderboard_screen()

                elif settings_btn.collidepoint(e.pos):
                    settings_screen(settings)

                elif quit_btn.collidepoint(e.pos):
                    save_settings(settings)
                    pygame.quit()
                    sys.exit()


main_menu()  # program starts here