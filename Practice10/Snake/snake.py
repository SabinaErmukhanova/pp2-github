import pygame
from pygame.locals import *
import random
import sys

pygame.init()
pygame.mixer.init()

#  SETTINGS 
WIDTH = 600
HEIGHT = 400
CELL = 20
SPEED = 5

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

#  SOUND 
pygame.mixer.music.load("sounds/music.mp3")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

eat_sound = pygame.mixer.Sound("sounds/gc.wav")
eat_sound.set_volume(1.0)

# COLORS 
SNAKE_COLOR = (170, 200, 50)
FOOD_COLOR = (255, 150, 0)

#  SCORE 
score = 0
level = 1

font = pygame.font.SysFont("Verdana", 20)

clock = pygame.time.Clock()

#  GAME OVER FUNCTION 
def game_over():
    screen.fill((255, 0, 0))

    big_font = pygame.font.SysFont("Verdana", 50)
    small_font = pygame.font.SysFont("Verdana", 25)

    text1 = big_font.render("GAME OVER", True, (0, 0, 0))
    text2 = small_font.render(f"Score: {score}", True, (0, 0, 0))
    text3 = small_font.render(f"Level: {level}", True, (0, 0, 0))

    screen.blit(text1, (WIDTH//2 - 150, HEIGHT//2 - 60))
    screen.blit(text2, (WIDTH//2 - 70, HEIGHT//2))
    screen.blit(text3, (WIDTH//2 - 70, HEIGHT//2 + 30))

    pygame.display.update()
    pygame.time.delay(2000)

    pygame.quit()
    sys.exit()

#  SNAKE 
snake = [[100,100],[130,100],[160,100]]
direction = "RIGHT"

#  FOOD
def spawn_food():
    while True:
        food = [
            random.randrange(0, WIDTH, CELL),
            random.randrange(0, HEIGHT, CELL)
        ]
        if food not in snake:
            return food

food = spawn_food()

#  GAME LOOP 
while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if keys[K_UP] and direction != "DOWN":
        direction = "UP"
    elif keys[K_DOWN] and direction != "UP":
        direction = "DOWN"
    elif keys[K_LEFT] and direction != "RIGHT":
        direction = "LEFT"
    elif keys[K_RIGHT] and direction != "LEFT":
        direction = "RIGHT"

    #  MOVE 
    head = snake[-1].copy()

    if direction == "RIGHT":
        head[0] += CELL
    elif direction == "LEFT":
        head[0] -= CELL
    elif direction == "UP":
        head[1] -= CELL
    elif direction == "DOWN":
        head[1] += CELL

    #  COLLISION (WALL) 
    if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
        game_over()

    #  COLLISION (SELF) 
    if head in snake:
        game_over()

    snake.append(head)

    #  EAT 
    if head == food:
        eat_sound.play()
        score += 1
        food = spawn_food()

        # LEVEL UP
        if score % 4 == 0:
            level += 1
            SPEED += 1
    else:
        snake.pop(0)

    #  DRAW 
    screen.fill((255,255,255))

    # snake
    for segment in snake:
        pygame.draw.rect(screen, SNAKE_COLOR,
                         pygame.Rect(segment[0], segment[1], CELL, CELL))

    # food
    pygame.draw.rect(screen, FOOD_COLOR,
                     pygame.Rect(food[0], food[1], CELL, CELL))

    # UI
    score_text = font.render(f"Score: {score}", True, (0,0,0))
    level_text = font.render(f"Level: {level}", True, (0,0,0))

    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 35))

    pygame.display.update()
    clock.tick(SPEED)