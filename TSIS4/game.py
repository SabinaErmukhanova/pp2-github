import pygame  # graphics, drawing, events, sound
import random  # randomness for spawning
from pygame.locals import *  # key constants like K_UP, QUIT
from db import save_result, get_best  # database functions

WIDTH = 600  # window width
HEIGHT = 400  # window height
CELL = 20  # size of one grid step

WHITE = (255, 255, 255)  # background
BLACK = (0, 0, 0)  # text
GRID_COLOR = (220, 220, 220)  # grid lines
OBSTACLE_COLOR = (40, 40, 40)  # fallback obstacle color

# file paths for images
FOOD_IMG = "assets/photo/apple.png"
POISON_IMG = "assets/photo/poison.png"
BOOST_IMG = "assets/photo/boost.png"
SLOW_IMG = "assets/photo/slow.png"
SHIELD_IMG = "assets/photo/shield.png"
OBSTACLE_IMG = "assets/photo/brick.png"

# file paths for sounds
MUSIC = "assets/sound/music.mp3"
EAT_SOUND = "assets/sound/gc.wav"
POISON_SOUND = "assets/sound/damage.mp3"
BOOST_SOUND = "assets/sound/nitro.mp3"
SLOW_SOUND = "assets/sound/slow.mp3"
SHIELD_SOUND = "assets/sound/shield.mp3"


def load_image(path, size):
    # loads image and resizes it
    try:
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (size, size))
    except:
        return None  # prevents crash if file missing


def load_sound(path):
    # loads sound safely
    try:
        return pygame.mixer.Sound(path)
    except:
        return None


def run_game(screen, username, settings):
    # main gameplay function

    pygame.mixer.init()
    clock = pygame.time.Clock()

    # read settings
    snake_color = tuple(settings.get("snake_color", [170, 200, 50]))
    sound_on = settings.get("sound", True)
    grid_on = settings.get("grid", False)

    font = pygame.font.SysFont("Verdana", 18)

    # load assets
    food_img = load_image(FOOD_IMG, CELL)
    poison_img = load_image(POISON_IMG, CELL)
    boost_img = load_image(BOOST_IMG, CELL)
    slow_img = load_image(SLOW_IMG, CELL)
    shield_img = load_image(SHIELD_IMG, CELL)
    obstacle_img = load_image(OBSTACLE_IMG, CELL)

    eat_sound = load_sound(EAT_SOUND)
    poison_sound = load_sound(POISON_SOUND)
    boost_sound = load_sound(BOOST_SOUND)
    slow_sound = load_sound(SLOW_SOUND)
    shield_sound = load_sound(SHIELD_SOUND)

    # background music logic
    if sound_on:
        try:
            pygame.mixer.music.load(MUSIC)
            pygame.mixer.music.play(-1)
        except:
            pass
    else:
        pygame.mixer.music.stop()

    # get best score from DB
    best_score = get_best(username) or 0

    # snake initial state
    snake = [[100, 100], [120, 100], [140, 100]]
    direction = "RIGHT"

    # game variables
    score = 0
    level = 1
    speed = 5

    food = None
    food_value = 1
    food_time = 0

    poison = None
    poison_time = 0

    power = None
    power_type = None
    power_spawn_time = 0

    active_power = None
    active_power_time = 0

    obstacles = []
    shield_ready = False

    def random_cell():
        # returns random grid-aligned position
        return [
            random.randrange(0, WIDTH, CELL),
            random.randrange(0, HEIGHT, CELL)
        ]

    def blocked_positions():
        # collects all occupied positions to avoid overlaps
        blocked = []
        blocked.extend(snake)
        blocked.extend(obstacles)

        if food:
            blocked.append(food)
        if poison:
            blocked.append(poison)
        if power:
            blocked.append(power)

        return blocked

    def spawn_position():
        # finds free cell not occupied by anything
        while True:
            pos = random_cell()
            if pos not in blocked_positions():
                return pos

    def spawn_food():
        # creates food with value and timestamp
        value = random.choices([1, 2, 3], weights=[70, 20, 10])[0]
        pos = spawn_position()
        return pos, value, pygame.time.get_ticks()

    def create_obstacles():
        # creates obstacles only from level 3
        new = []
        if level < 3:
            return new

        amount = min(4 + level, 12)

        while len(new) < amount:
            pos = random_cell()

            # prevent spawning too close to snake head
            near_head = abs(pos[0] - snake[-1][0]) <= CELL*2 and abs(pos[1] - snake[-1][1]) <= CELL*2

            if pos not in snake and pos not in new and not near_head:
                new.append(pos)

        return new

    # first food spawn
    food, food_value, food_time = spawn_food()

    running = True

    while running:

        # event handling (keyboard + exit)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.mixer.music.stop()
                save_result(username, score, level)
                return {"score": score, "level": level, "best": best_score}

            if event.type == KEYDOWN:
                # direction change logic (prevents reverse)
                if event.key == K_UP and direction != "DOWN":
                    direction = "UP"
                elif event.key == K_DOWN and direction != "UP":
                    direction = "DOWN"
                elif event.key == K_LEFT and direction != "RIGHT":
                    direction = "LEFT"
                elif event.key == K_RIGHT and direction != "LEFT":
                    direction = "RIGHT"

        # copy current head position
        head = snake[-1].copy()

        # move head depending on direction
        if direction == "RIGHT":
            head[0] += CELL
        elif direction == "LEFT":
            head[0] -= CELL
        elif direction == "UP":
            head[1] -= CELL
        elif direction == "DOWN":
            head[1] += CELL

        # collision detection
        hit_wall = head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT
        hit_self = head in snake
        hit_obstacle = head in obstacles

        # collision response
        if hit_wall or hit_self or hit_obstacle:
            if shield_ready:
                # shield cancels one hit
                shield_ready = False
                active_power = None
                head = snake[-1].copy()
            else:
                running = False  # game over

        if running:
            snake.append(head)  # add new head

            ate_food = head == food
            ate_poison = poison and head == poison
            ate_power = power and head == power

            if ate_food:
                # normal food increases score
                if sound_on and eat_sound:
                    eat_sound.play()

                score += food_value
                food, food_value, food_time = spawn_food()

                # level increases every 5 score
                if score // 5 + 1 > level:
                    level += 1
                    speed += 1
                    obstacles = create_obstacles()

            elif ate_poison:
                # poison reduces snake length
                if sound_on and poison_sound:
                    poison_sound.play()

                poison = None

                if len(snake) <= 3:
                    running = False
                else:
                    snake.pop(0)
                    snake.pop(0)
                    snake.pop(0)

            elif ate_power:
                # activate power-up
                if power_type == "boost":
                    active_power = "boost"
                elif power_type == "slow":
                    active_power = "slow"
                elif power_type == "shield":
                    active_power = "shield"
                    shield_ready = True

                active_power_time = pygame.time.get_ticks()
                power = None
                power_type = None

            else:
                snake.pop(0)  # normal movement removes tail

        current_time = pygame.time.get_ticks()

        # food expires after 8 seconds
        if current_time - food_time > 8000:
            food, food_value, food_time = spawn_food()

        # poison spawn chance
        if poison is None and random.randint(1, 100) <= 2:
            poison = spawn_position()
            poison_time = current_time

        # poison disappears after time
        if poison and current_time - poison_time > 8000:
            poison = None

        # power-up spawn chance
        if power is None and random.randint(1, 100) <= 2:
            power = spawn_position()
            power_type = random.choice(["boost", "slow", "shield"])
            power_spawn_time = current_time

        # power-up disappears
        if power and current_time - power_spawn_time > 8000:
            power = None
            power_type = None

        final_speed = speed

        # active power effects
        if active_power == "boost":
            final_speed = speed + 4
            if current_time - active_power_time > 5000:
                active_power = None

        elif active_power == "slow":
            final_speed = max(3, speed - 3)
            if current_time - active_power_time > 5000:
                active_power = None

        # drawing section
        screen.fill(WHITE)

        # draw grid if enabled
        if grid_on:
            for x in range(0, WIDTH, CELL):
                pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))
            for y in range(0, HEIGHT, CELL):
                pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))

        # draw obstacles
        for block in obstacles:
            if obstacle_img:
                screen.blit(obstacle_img, (block[0], block[1]))
            else:
                pygame.draw.rect(screen, OBSTACLE_COLOR, (block[0], block[1], CELL, CELL))

        # draw snake
        for segment in snake:
            pygame.draw.rect(screen, snake_color, (segment[0], segment[1], CELL, CELL))

        # draw food
        if food:
            if food_img:
                screen.blit(food_img, (food[0], food[1]))
            else:
                pygame.draw.rect(screen, (255,150,0), (food[0], food[1], CELL, CELL))

        # draw poison
        if poison:
            if poison_img:
                screen.blit(poison_img, (poison[0], poison[1]))
            else:
                pygame.draw.rect(screen, (100,0,0), (poison[0], poison[1], CELL, CELL))

        # draw power-ups
        if power:
            img = boost_img if power_type=="boost" else slow_img if power_type=="slow" else shield_img
            if img:
                screen.blit(img, (power[0], power[1]))

        # UI text
        screen.blit(font.render(f"Player: {username}", True, BLACK), (10, 10))
        screen.blit(font.render(f"Score: {score}", True, BLACK), (10, 35))
        screen.blit(font.render(f"Level: {level}", True, BLACK), (10, 60))
        screen.blit(font.render(f"Best: {best_score}", True, BLACK), (10, 85))

        pygame.display.update()
        clock.tick(final_speed)

    pygame.mixer.music.stop()
    save_result(username, score, level)

    return {"score": score, "level": level, "best": best_score}