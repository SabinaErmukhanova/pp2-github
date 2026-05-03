import pygame                         # import pygame library for graphics, input and sound
from pygame.locals import *           # import pygame constants like QUIT, KEYDOWN, etc.
import random                         # import random for generating food positions and values
import sys                            # import sys for exiting the program

pygame.init()                         # initialize all pygame modules
pygame.mixer.init()                  # initialize sound system

# WINDOW SETTINGS
WIDTH = 600                          # window width in pixels
HEIGHT = 400                         # window height in pixels
CELL = 20                            # size of one grid cell (snake moves by this amount)

screen = pygame.display.set_mode((WIDTH, HEIGHT))   # create game window
pygame.display.set_caption("Snake")  # set window title

# SOUND
pygame.mixer.music.load("sound/music.mp3")   # load background music file
pygame.mixer.music.set_volume(0.2)           # set music volume (20%)
pygame.mixer.music.play(-1)                  # play music in loop (-1 means infinite)

eat_sound = pygame.mixer.Sound("sound/gc.wav")   # load sound for eating food

# COLORS
SNAKE_COLOR = (170, 200, 50)       # color of snake (light green)

# GAME VARIABLES
score = 0                          # player score
level = 1                          # current level
speed = 2                          # game speed (FPS, controls snake speed)

font = pygame.font.SysFont("Verdana", 20)   # font for UI text
clock = pygame.time.Clock()                 # clock to control FPS

# GAME OVER FUNCTION
def game_over():
    screen.fill((255, 0, 0))      # fill screen with red color

    big_font = pygame.font.SysFont("Verdana", 50)    # large font for title
    small_font = pygame.font.SysFont("Verdana", 25)  # smaller font for info

    text1 = big_font.render("GAME OVER", True, (0, 0, 0))  # render "Game Over"
    text2 = small_font.render(f"Score: {score}", True, (0, 0, 0))  # render score
    text3 = small_font.render(f"Level: {level}", True, (0, 0, 0))  # render level

    # draw texts on screen
    screen.blit(text1, (WIDTH//2 - 150, HEIGHT//2 - 60))
    screen.blit(text2, (WIDTH//2 - 70, HEIGHT//2))
    screen.blit(text3, (WIDTH//2 - 70, HEIGHT//2 + 30))

    pygame.display.update()       # update screen
    pygame.time.delay(2000)       # wait 2 seconds

    pygame.quit()                 # close pygame
    sys.exit()                    # exit program

# SNAKE INITIAL STATE
snake = [[100,100],[120,100],[140,100]]   # list of snake segments (x,y positions)
direction = "RIGHT"                       # initial movement direction

# FOOD SPAWN FUNCTION (with weight and timer)
def spawn_food():
    while True:                           # loop until valid position found
        food = [
            random.randrange(0, WIDTH, CELL),   # random x position aligned to grid
            random.randrange(0, HEIGHT, CELL)   # random y position aligned to grid
        ]
        if food not in snake:              # ensure food is not inside snake
            # randomly choose food value with probabilities
            value = random.choices([1,2,3], weights=[70,20,10])[0]
            spawn_time = pygame.time.get_ticks()   # record spawn time (ms since game start)
            return food, value, spawn_time         # return position, value, and time

# FIRST FOOD CREATION
food, food_value, food_time = spawn_food()   # initialize first food

# MAIN GAME LOOP
while True:

    for event in pygame.event.get():        # handle all events
        if event.type == QUIT:              # if user closes window
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:           # if key is pressed
            # change direction but prevent reverse movement
            if event.key == K_UP and direction != "DOWN":
                direction = "UP"
            elif event.key == K_DOWN and direction != "UP":
                direction = "DOWN"
            elif event.key == K_LEFT and direction != "RIGHT":
                direction = "LEFT"
            elif event.key == K_RIGHT and direction != "LEFT":
                direction = "RIGHT"

    # MOVE SNAKE
    head = snake[-1].copy()    # take current head position

    # update head position based on direction
    if direction == "RIGHT":
        head[0] += CELL
    elif direction == "LEFT":
        head[0] -= CELL
    elif direction == "UP":
        head[1] -= CELL
    elif direction == "DOWN":
        head[1] += CELL

    # WALL COLLISION CHECK
    if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
        game_over()

    # SELF COLLISION CHECK
    if head in snake:
        game_over()

    snake.append(head)   # add new head to snake

    # FOOD COLLISION
    if head == food:
        eat_sound.play()        # play eating sound
        score += food_value     # increase score by food value

        food, food_value, food_time = spawn_food()   # spawn new food

        # LEVEL UP (every 2 score points)
        if score % 2 == 0:
            level += 1
            speed += 1          # increase game speed

    else:
        snake.pop(0)            # remove tail if no food eaten

    # FOOD TIMER (food disappears)
    current_time = pygame.time.get_ticks()   # get current time

    if current_time - food_time > 10000:     # if food exists longer than 10 seconds
        food, food_value, food_time = spawn_food()

    # SECOND TIMER (also removes food faster)
    current_time = pygame.time.get_ticks()
    if current_time - food_time > 5000:      # if food exists longer than 5 seconds
        food, food_value, food_time = spawn_food()

    # DRAW EVERYTHING
    screen.fill((255,255,255))   # clear screen with white

    # DRAW SNAKE
    for segment in snake:
        pygame.draw.rect(screen, SNAKE_COLOR,
                         pygame.Rect(segment[0], segment[1], CELL, CELL))

    # FOOD COLOR BASED ON VALUE
    if food_value == 1:
        color = (255,150,0)     # orange (common)
    elif food_value == 2:
        color = (0,200,255)     # blue (medium)
    else:
        color = (255,0,0)       # red (rare)

    # DRAW FOOD
    pygame.draw.rect(screen, color,
                     pygame.Rect(food[0], food[1], CELL, CELL))

    # DRAW UI TEXT
    score_text = font.render(f"Score: {score}", True, (0,0,0))
    level_text = font.render(f"Level: {level}", True, (0,0,0))

    screen.blit(score_text, (10, 10))   # display score
    screen.blit(level_text, (10, 35))   # display level

    pygame.display.update()             # update screen

    # CONTROL SPEED
    clock.tick(speed)                   # set FPS (higher = faster snake)