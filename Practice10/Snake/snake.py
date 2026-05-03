import pygame
from pygame.locals import *
import random
import sys

pygame.init()
pygame.mixer.init()

# WINDOW SETTINGS
WIDTH = 600
HEIGHT = 400
CELL = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

# SOUND
pygame.mixer.music.load("sounds/music.mp3")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

eat_sound = pygame.mixer.Sound("sounds/gc.wav")

# COLORS
SNAKE_COLOR = (170, 200, 50)
FOOD_COLOR = (255, 150, 0)

# GAME VARIABLES
score = 0
level = 1
speed = 2  # 🔥 начальная скорость (как просил преподаватель)

font = pygame.font.SysFont("Verdana", 20)
clock = pygame.time.Clock()

# GAME OVER
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

# SNAKE
snake = [[100,100],[120,100],[140,100]]
direction = "RIGHT"

# FOOD
def spawn_food():
    while True:
        food = [
            random.randrange(0, WIDTH, CELL),
            random.randrange(0, HEIGHT, CELL)
        ]
        if food not in snake:
            return food

food = spawn_food()

# GAME LOOP
while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_UP and direction != "DOWN":
                direction = "UP"
            elif event.key == K_DOWN and direction != "UP":
                direction = "DOWN"
            elif event.key == K_LEFT and direction != "RIGHT":
                direction = "LEFT"
            elif event.key == K_RIGHT and direction != "LEFT":
                direction = "RIGHT"

    # MOVE
    head = snake[-1].copy()

    if direction == "RIGHT":
        head[0] += CELL
    elif direction == "LEFT":
        head[0] -= CELL
    elif direction == "UP":
        head[1] -= CELL
    elif direction == "DOWN":
        head[1] += CELL

    # WALL COLLISION
    if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
        game_over()

    # SELF COLLISION
    if head in snake:
        game_over()

    snake.append(head)

    # EAT FOOD
    if head == food:
        eat_sound.play()
        score += 1
        food = spawn_food()

        # 🔥 LEVEL UP (каждые 2 яблока)
        if score % 2 == 0:
            level += 1
            speed += 1   # 🔥 вот главное — скорость увеличивается на 1

    else:
        snake.pop(0)

    # DRAW
    screen.fill((255,255,255))

    for segment in snake:
        pygame.draw.rect(screen, SNAKE_COLOR,
                         pygame.Rect(segment[0], segment[1], CELL, CELL))

    pygame.draw.rect(screen, FOOD_COLOR,
                     pygame.Rect(food[0], food[1], CELL, CELL))

    score_text = font.render(f"Score: {score}", True, (0,0,0))
    level_text = font.render(f"Level: {level}", True, (0,0,0))

    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 35))

    pygame.display.update()

    # 🔥 скорость змеи зависит от level
    clock.tick(speed)