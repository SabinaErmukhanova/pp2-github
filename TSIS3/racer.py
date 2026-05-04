import pygame  # imports pygame library for graphics, events, sounds, images, and game window
import random  # imports random library to randomly choose lanes, enemies, coins, obstacles, and power-ups
from pygame.locals import *  # imports pygame constants like QUIT, K_LEFT, K_RIGHT, and USEREVENT

WIDTH = 700  # width of the game window
HEIGHT = 500  # height of the game window

LANES = [150, 350, 550]  # x-coordinates of road lanes where objects can spawn
WHITE = (255, 255, 255)  # white color used for text


def colorize_car(image, color_name):  # function that changes player car color based on settings
    if color_name == "default":  # if default color is selected
        return image  # return original image without changes

    color_map = {  # dictionary that connects color names with RGBA color values
        "red": (255, 80, 80, 255),  # red tint
        "blue": (80, 120, 255, 255),  # blue tint
        "green": (80, 255, 120, 255),  # green tint
        "yellow": (255, 255, 80, 255)  # yellow tint
    }

    copy = image.copy()  # creates a copy of the original image so the original is not changed
    tint = pygame.Surface(copy.get_size(), pygame.SRCALPHA)  # creates transparent surface with same size as image
    tint.fill(color_map[color_name])  # fills tint surface with selected color
    copy.blit(tint, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)  # applies color tint to image

    return copy  # returns recolored image


def run_game(screen, username, settings):  # main game function, called from main.py
    pygame.mixer.init()  # initializes pygame sound system

    clock = pygame.time.Clock()  # creates clock object to control FPS

    if settings["difficulty"] == "easy":  # checks if difficulty is easy
        BASE_SPEED = 3  # sets slow base speed
        enemy_time = 1900  # enemies spawn every 1900 milliseconds
        obstacle_time = 2600  # obstacles spawn every 2600 milliseconds
    elif settings["difficulty"] == "medium":  # checks if difficulty is medium
        BASE_SPEED = 4  # sets normal base speed
        enemy_time = 1500  # enemies spawn every 1500 milliseconds
        obstacle_time = 2100  # obstacles spawn every 2100 milliseconds
    else:  # if difficulty is hard
        BASE_SPEED = 5  # sets faster base speed
        enemy_time = 1100  # enemies spawn more often
        obstacle_time = 1600  # obstacles spawn more often

    SPEED = BASE_SPEED  # current game speed starts as base speed

    score = 0  # current score of the player
    coins_collected = 0  # total coin value collected by player
    distance = 0  # distance travelled during the game
    lives = 3  # player starts with 3 lives

    active_power = None  # stores currently active power-up
    power_timer = 0  # stores time when power-up was activated

    bg = pygame.image.load("photo/road.png").convert_alpha()  # loads road background image
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))  # scales background to fit window size

    bg_y1 = 0  # first background y-position
    bg_y2 = -HEIGHT  # second background y-position for infinite scrolling

    heart = pygame.image.load("photo/health.png").convert_alpha()  # loads heart image for lives
    heart = pygame.transform.scale(heart, (28, 28))  # resizes heart image

    font = pygame.font.SysFont("Verdana", 18)  # creates font for UI text

    if settings["sound"]:  # checks if sound is enabled in settings
        coin_sound = pygame.mixer.Sound("sound/gc.mp3")  # loads coin collection sound
        crash_sound = pygame.mixer.Sound("sound/crash.mp3")  # loads crash damage sound
        nitro_sound = pygame.mixer.Sound("sound/nitro.mp3")  # loads nitro sound
        shield_sound = pygame.mixer.Sound("sound/shield.mp3")  # loads shield sound
        heal_sound = pygame.mixer.Sound("sound/healing.mp3")  # loads repair healing sound

        pygame.mixer.music.load("sound/music.mp3")  # loads background music
        pygame.mixer.music.set_volume(0.3)  # sets music volume
        pygame.mixer.music.play(-1)  # plays music forever in loop
    else:  # if sound is disabled
        coin_sound = None  # no coin sound
        crash_sound = None  # no crash sound
        nitro_sound = None  # no nitro sound
        shield_sound = None  # no shield sound
        heal_sound = None  # no healing sound
        pygame.mixer.music.stop()  # stops background music

    class Player(pygame.sprite.Sprite):  # class for player car
        def __init__(self):  # constructor method for player
            super().__init__()  # initializes parent Sprite class

            img = pygame.image.load("photo/player.png").convert_alpha()  # loads player car image
            rect = img.get_bounding_rect()  # finds visible part of image and removes transparent borders
            img = img.subsurface(rect).copy()  # crops image to visible area

            img = pygame.transform.scale(img, (110, 130))  # resizes player car image
            img = colorize_car(img, settings["car_color"])  # applies selected car color from settings

            self.image = img  # stores final player image
            self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 85))  # places player near bottom center
            self.hitbox = self.rect.inflate(-50, -55)  # creates smaller collision rectangle
            self.speed = 6  # player movement speed

        def move(self):  # method for moving player
            keys = pygame.key.get_pressed()  # gets currently pressed keyboard keys

            if keys[K_LEFT]:  # if left arrow is pressed
                self.rect.x -= self.speed  # move player left

            if keys[K_RIGHT]:  # if right arrow is pressed
                self.rect.x += self.speed  # move player right

            if self.rect.left < 0:  # if player goes beyond left border
                self.rect.left = 0  # keep player inside left border

            if self.rect.right > WIDTH:  # if player goes beyond right border
                self.rect.right = WIDTH  # keep player inside right border

            self.hitbox.center = self.rect.center  # keep hitbox centered on image

    class Enemy(pygame.sprite.Sprite):  # class for enemy traffic cars
        def __init__(self):  # constructor method for enemy
            super().__init__()  # initializes parent Sprite class

            img_name = random.choice(["enemy1.png", "enemy2.png", "enemy3.png"])  # randomly selects enemy image
            img = pygame.image.load("photo/" + img_name).convert_alpha()  # loads selected enemy image
            img = pygame.transform.rotate(img, 180)

            rect = img.get_bounding_rect()  # finds visible part of enemy image
            img = img.subsurface(rect).copy()  # crops transparent borders from enemy image

            self.image = pygame.transform.scale(img, (75, 105))  # resizes enemy car image
            self.rect = self.image.get_rect(center=(random.choice(LANES), -80))  # spawns enemy above screen
            self.hitbox = self.rect.inflate(-40, -45)  # creates smaller collision rectangle for enemy

        def move(self):  # method for moving enemy
            self.rect.y += SPEED + 1  # moves enemy downward slightly faster than road speed
            self.hitbox.center = self.rect.center  # keeps enemy hitbox aligned with image

            if self.rect.top > HEIGHT:  # if enemy moves below screen
                self.kill()  # removes enemy from group

    class Coin(pygame.sprite.Sprite):  # class for collectible coins
        def __init__(self):  # constructor method for coin
            super().__init__()  # initializes parent Sprite class

            self.value = random.choices([1, 2, 3], weights=[70, 20, 10])[0]  # chooses coin value with probabilities

            if self.value == 1:  # if coin is normal value
                img = pygame.image.load("photo/coin.png").convert_alpha()  # loads coin image
                size = 35  # normal coin size
            elif self.value == 2:  # if coin is medium value
                img = pygame.image.load("photo/diamond.png").convert_alpha()  # loads diamond image
                size = 42  # diamond size
            else:  # if coin is rare value
                img = pygame.image.load("photo/rare.png").convert_alpha()  # loads rare coin image
                size = 48  # rare coin size

            self.image = pygame.transform.scale(img, (size, size))  # resizes coin image
            self.rect = self.image.get_rect(center=(random.choice(LANES), -40))  # spawns coin above screen
            self.hitbox = self.rect.inflate(-10, -10)  # creates smaller coin collision rectangle

        def move(self):  # method for moving coin
            self.rect.y += SPEED  # moves coin downward
            self.hitbox.center = self.rect.center  # keeps coin hitbox aligned with image

            if self.rect.top > HEIGHT:  # if coin moves below screen
                self.kill()  # removes coin from group

    class Obstacle(pygame.sprite.Sprite):  # class for obstacles such as oil, hole, barrier
        def __init__(self):  # constructor method for obstacle
            super().__init__()  # initializes parent Sprite class

            self.type = random.choice(["oil", "hole", "barrier"])  # randomly chooses obstacle type

            img = pygame.image.load(f"photo/{self.type}.png").convert_alpha()  # loads obstacle image based on type
            self.image = pygame.transform.scale(img, (85, 85))  # resizes obstacle image
            self.rect = self.image.get_rect(center=(random.choice(LANES), -60))  # spawns obstacle above screen
            self.hitbox = self.rect.inflate(-30, -30)  # creates smaller collision rectangle for obstacle

        def move(self):  # method for moving obstacle
            self.rect.y += SPEED  # moves obstacle downward
            self.hitbox.center = self.rect.center  # keeps obstacle hitbox aligned with image

            if self.rect.top > HEIGHT:  # if obstacle moves below screen
                self.kill()  # removes obstacle from group

    class PowerUp(pygame.sprite.Sprite):  # class for nitro, shield, and repair power-ups
        def __init__(self):  # constructor method for power-up
            super().__init__()  # initializes parent Sprite class

            self.type = random.choices(  # randomly chooses power-up type with probabilities
                ["nitro", "shield", "repair"],  # possible power-up types
                weights=[30, 30, 40]  # repair has slightly higher chance
            )[0]  # gets selected result

            img_map = {  # maps power-up type to image file
                "nitro": "boost.png",  # nitro uses boost image
                "shield": "shield.png",  # shield uses shield image
                "repair": "repair.png"  # repair uses repair image
            }

            img = pygame.image.load("photo/" + img_map[self.type]).convert_alpha()  # loads power-up image
            self.image = pygame.transform.scale(img, (75, 75))  # resizes power-up image
            self.rect = self.image.get_rect(center=(random.choice(LANES), -60))  # spawns power-up above screen
            self.hitbox = self.rect.inflate(-20, -20)  # creates smaller collision rectangle for power-up
            self.spawn_time = pygame.time.get_ticks()  # stores spawn time for timeout

        def move(self):  # method for moving power-up
            self.rect.y += SPEED  # moves power-up downward
            self.hitbox.center = self.rect.center  # keeps power-up hitbox aligned with image

            if self.rect.top > HEIGHT:  # if power-up moves below screen
                self.kill()  # removes power-up from group

            if pygame.time.get_ticks() - self.spawn_time > 6000:  # if power-up exists more than 6 seconds
                self.kill()  # removes power-up after timeout

    player = Player()  # creates player object

    enemies = pygame.sprite.Group()  # group for enemy cars
    coins = pygame.sprite.Group()  # group for coins
    obstacles = pygame.sprite.Group()  # group for obstacles
    powers = pygame.sprite.Group()  # group for power-ups

    ADD_ENEMY = pygame.USEREVENT + 1  # custom event for spawning enemies
    ADD_COIN = pygame.USEREVENT + 2  # custom event for spawning coins
    ADD_OBSTACLE = pygame.USEREVENT + 3  # custom event for spawning obstacles
    ADD_POWER = pygame.USEREVENT + 4  # custom event for spawning power-ups

    pygame.time.set_timer(ADD_ENEMY, enemy_time)  # sets enemy spawn interval
    pygame.time.set_timer(ADD_COIN, 1200)  # sets coin spawn interval
    pygame.time.set_timer(ADD_OBSTACLE, obstacle_time)  # sets obstacle spawn interval
    pygame.time.set_timer(ADD_POWER, 5000)  # sets power-up spawn interval

    def damage():  # function that handles damage to player
        nonlocal lives  # allows changing lives variable from outer function

        if active_power != "shield":  # if shield is not active
            if crash_sound:  # if crash sound exists
                crash_sound.play()  # plays crash sound

            lives -= 1  # removes one life from player

    while True:  # main game loop
        for event in pygame.event.get():  # processes all pygame events
            if event.type == QUIT:  # if window close button is pressed
                pygame.mixer.music.stop()  # stops background music
                return {  # returns game result to main.py
                    "name": username,  # player name
                    "score": int(score),  # final score
                    "distance": int(distance),  # final distance
                    "coins": coins_collected  # collected coins
                }

            if event.type == ADD_ENEMY:  # if enemy spawn event happens
                enemies.add(Enemy())  # creates and adds enemy to enemy group

            if event.type == ADD_COIN:  # if coin spawn event happens
                coins.add(Coin())  # creates and adds coin to coin group

            if event.type == ADD_OBSTACLE:  # if obstacle spawn event happens
                obstacles.add(Obstacle())  # creates and adds obstacle to obstacle group

            if event.type == ADD_POWER:  # if power-up spawn event happens
                powers.add(PowerUp())  # creates and adds power-up to power group

        bg_y1 += SPEED  # moves first background down
        bg_y2 += SPEED  # moves second background down

        if bg_y1 >= HEIGHT:  # if first background leaves screen
            bg_y1 = -HEIGHT  # move it back above screen

        if bg_y2 >= HEIGHT:  # if second background leaves screen
            bg_y2 = -HEIGHT  # move it back above screen

        screen.blit(bg, (0, bg_y1))  # draws first background
        screen.blit(bg, (0, bg_y2))  # draws second background

        player.move()  # updates player position
        screen.blit(player.image, player.rect)  # draws player image

        for enemy in enemies:  # loops through enemy objects
            enemy.move()  # moves enemy
            screen.blit(enemy.image, enemy.rect)  # draws enemy

        for coin in coins:  # loops through coin objects
            coin.move()  # moves coin
            screen.blit(coin.image, coin.rect)  # draws coin

        for obstacle in obstacles:  # loops through obstacle objects
            obstacle.move()  # moves obstacle
            screen.blit(obstacle.image, obstacle.rect)  # draws obstacle

        for power in powers:  # loops through power-up objects
            power.move()  # moves power-up
            screen.blit(power.image, power.rect)  # draws power-up

        for enemy in enemies:  # checks collision with enemies
            if player.hitbox.colliderect(enemy.hitbox):  # if player hitbox touches enemy hitbox
                damage()  # apply damage
                enemy.kill()  # remove enemy after collision

        for obstacle in obstacles:  # checks collision with obstacles
            if player.hitbox.colliderect(obstacle.hitbox):  # if player touches obstacle
                damage()  # apply damage

                if obstacle.type == "oil" and active_power != "shield":  # if obstacle is oil and shield is not active
                    player.rect.x += random.choice([-60, 60])  # slide player left or right

                obstacle.kill()  # remove obstacle after collision

        for coin in coins:  # checks collision with coins
            if player.hitbox.colliderect(coin.hitbox):  # if player collects coin
                if coin_sound:  # if coin sound exists
                    coin_sound.play()  # play coin sound

                score += coin.value * 10  # increase score based on coin value
                coins_collected += coin.value  # increase collected coins counter
                coin.kill()  # remove coin after collection

        for power in powers:  # checks collision with power-ups
            if player.hitbox.colliderect(power.hitbox):  # if player collects power-up
                if power.type == "nitro":  # if power-up is nitro
                    if nitro_sound:  # if nitro sound exists
                        nitro_sound.play()  # play nitro sound

                    active_power = "nitro"  # activate nitro
                    power_timer = pygame.time.get_ticks()  # save activation time

                elif power.type == "shield":  # if power-up is shield
                    if shield_sound:  # if shield sound exists
                        shield_sound.play()  # play shield sound

                    active_power = "shield"  # activate shield
                    power_timer = pygame.time.get_ticks()  # save activation time

                elif power.type == "repair":  # if power-up is repair
                    if heal_sound:  # if healing sound exists
                        heal_sound.play()  # play healing sound

                    lives = min(3, lives + 1)  # add one life but maximum is 3
                    active_power = None  # repair is instant, so no active power remains

                power.kill()  # remove collected power-up

        if active_power == "nitro":  # if nitro is active
            SPEED = BASE_SPEED + 2  # increase speed by 2

            if pygame.time.get_ticks() - power_timer > 5000:  # if 5 seconds passed
                SPEED = BASE_SPEED  # return speed to normal
                active_power = None  # deactivate nitro

        elif active_power == "shield":  # if shield is active
            if pygame.time.get_ticks() - power_timer > 5000:  # if 5 seconds passed
                active_power = None  # deactivate shield

        distance += SPEED * 0.02  # increase distance based on speed
        score += 0.02  # slowly increase score over time

        if lives <= 0:  # if player has no lives
            pygame.mixer.music.stop()  # stop background music
            return {  # return final result to main.py
                "name": username,  # player name
                "score": int(score),  # final score
                "distance": int(distance),  # final distance
                "coins": coins_collected  # collected coins
            }

        for i in range(lives):  # draw one heart for each life
            screen.blit(heart, (10 + i * 34, 15))  # draw heart image

        screen.blit(font.render(f"Player: {username}", True, WHITE), (10, 52))  # draw player name
        screen.blit(font.render(f"Score: {int(score)}", True, WHITE), (WIDTH - 190, 10))  # draw score
        screen.blit(font.render(f"Coins: {coins_collected}", True, WHITE), (WIDTH - 190, 35))  # draw coins
        screen.blit(font.render(f"Dist: {int(distance)}", True, WHITE), (WIDTH - 190, 60))  # draw distance

        if active_power:  # if any power-up is active
            screen.blit(font.render(f"Power: {active_power}", True, WHITE), (WIDTH - 190, 85))  # draw active power-up

        pygame.display.update()  # updates screen
        clock.tick(60)  # limits game to 60 FPS