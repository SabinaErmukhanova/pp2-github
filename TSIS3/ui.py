import pygame  # imports pygame library for graphics, drawing, fonts, and events
import sys  # used to exit the program
from persistence import load_leaderboard, save_settings  # imports functions to load leaderboard and save settings

WHITE = (255, 255, 255)  # constant for white color used in text and borders


def draw_button(screen, text, rect, font):
    # function to draw a clickable button on the screen

    pygame.draw.rect(screen, (70, 70, 70), rect)  # draw button background (dark gray)
    pygame.draw.rect(screen, WHITE, rect, 2)  # draw white border around button

    label = font.render(text, True, WHITE)  # render button text in white color

    # draw text centered inside the button rectangle
    screen.blit(
        label,
        (
            rect.centerx - label.get_width() // 2,  # horizontal center alignment
            rect.centery - label.get_height() // 2  # vertical center alignment
        )
    )


def username_screen(screen, font_big, font, font_small):
    # screen where player enters their name before starting the game

    name = ""  # variable to store typed name

    while True:  # loop until user confirms or exits
        screen.fill((20, 20, 20))  # fill background with dark color

        # draw title
        title = font_big.render("Enter Name", True, WHITE)
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 80))

        # input box
        box = pygame.Rect(180, 180, 340, 55)
        pygame.draw.rect(screen, WHITE, box, 2)  # draw border for input box

        # render typed text
        text = font.render(name, True, WHITE)
        screen.blit(text, (box.x + 10, box.y + 12))  # draw text inside box

        # hint text
        hint = font_small.render("Press Enter to start", True, WHITE)
        screen.blit(hint, (screen.get_width() // 2 - hint.get_width() // 2, 260))

        pygame.display.update()  # update screen

        for event in pygame.event.get():  # handle events
            if event.type == pygame.QUIT:  # if window closed
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:  # if key pressed
                if event.key == pygame.K_RETURN and name.strip() != "":
                    return name.strip()  # return entered name (remove spaces)

                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]  # delete last character

                elif event.key == pygame.K_ESCAPE:
                    return None  # cancel and go back

                else:
                    name += event.unicode  # add typed character


def leaderboard_screen(screen, font_big, font, font_small):
    # screen to display top scores

    back_button = pygame.Rect(250, 420, 200, 50)  # button to return to menu

    while True:
        screen.fill((0, 0, 40))  # dark blue background

        # draw title
        title = font_big.render("Leaderboard", True, WHITE)
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 30))

        data = load_leaderboard()  # load scores from file

        y = 100  # starting vertical position for list

        if not data:
            # if no scores yet
            text = font.render("No scores yet", True, WHITE)
            screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 200))
        else:
            # display each score
            for i, row in enumerate(data):
                line = f"{i + 1}. {row.get('name', 'Unknown')} | Score: {row.get('score', 0)} | Dist: {row.get('distance', 0)} | Coins: {row.get('coins', 0)}"
                label = font_small.render(line, True, WHITE)
                screen.blit(label, (50, y))
                y += 28  # move down for next entry

        draw_button(screen, "Back", back_button, font)  # draw back button

        pygame.display.update()  # refresh screen

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    return  # go back to main menu


def settings_screen(screen, font_big, font, settings):
    # screen to modify game settings

    sound_button = pygame.Rect(190, 120, 320, 55)  # toggle sound
    difficulty_button = pygame.Rect(190, 200, 320, 55)  # change difficulty
    color_button = pygame.Rect(190, 280, 320, 55)  # change car color
    back_button = pygame.Rect(190, 380, 320, 55)  # return button

    difficulties = ["easy", "medium", "hard"]  # available difficulty levels
    colors = ["default", "red", "blue", "green", "yellow"]  # available car colors

    while True:
        screen.fill((30, 20, 20))  # dark background

        # draw title
        title = font_big.render("Settings", True, WHITE)
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 40))

        # draw buttons with current values
        draw_button(screen, "Sound: " + ("ON" if settings["sound"] else "OFF"), sound_button, font)
        draw_button(screen, "Difficulty: " + settings["difficulty"], difficulty_button, font)
        draw_button(screen, "Car color: " + settings["car_color"], color_button, font)
        draw_button(screen, "Back", back_button, font)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_settings(settings)  # save settings before exit
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if sound_button.collidepoint(event.pos):
                    settings["sound"] = not settings["sound"]  # toggle sound

                elif difficulty_button.collidepoint(event.pos):
                    index = difficulties.index(settings["difficulty"])  # current index
                    settings["difficulty"] = difficulties[(index + 1) % len(difficulties)]  # next option

                elif color_button.collidepoint(event.pos):
                    index = colors.index(settings["car_color"])  # current index
                    settings["car_color"] = colors[(index + 1) % len(colors)]  # next option

                elif back_button.collidepoint(event.pos):
                    save_settings(settings)  # save before returning
                    return


def game_over_screen(screen, font_big, font, result):
    # screen shown after game ends

    retry_button = pygame.Rect(220, 310, 260, 55)  # retry button
    menu_button = pygame.Rect(220, 390, 260, 55)  # main menu button

    while True:
        screen.fill((120, 0, 0))  # red background for game over

        # title
        title = font_big.render("GAME OVER", True, WHITE)
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 45))

        # show results
        score_text = font.render(f"Score: {result['score']}", True, WHITE)
        distance_text = font.render(f"Distance: {result['distance']}", True, WHITE)
        coins_text = font.render(f"Coins: {result['coins']}", True, WHITE)

        screen.blit(score_text, (240, 140))
        screen.blit(distance_text, (240, 180))
        screen.blit(coins_text, (240, 220))

        # draw buttons
        draw_button(screen, "Retry", retry_button, font)
        draw_button(screen, "Main Menu", menu_button, font)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_button.collidepoint(event.pos):
                    return "retry"  # restart game

                if menu_button.collidepoint(event.pos):
                    return "menu"  # go back to main menu