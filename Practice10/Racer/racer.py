import pygame, sys, random, time          # import libraries: pygame for game, sys for exit, random for spawning, time for delays
from pygame.locals import *              # import pygame constants like QUIT, K_LEFT, etc.

pygame.init()                            # initialize all pygame modules (graphics, input)
pygame.mixer.init()                      # initialize sound system

SCREEN_WIDTH = 600                       # width of game window
SCREEN_HEIGHT = 400                      # height of game window
SPEED = 5                                # speed of enemies and background movement
SCORE = 0                                # player score (coins collected)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))   # create game window
pygame.display.set_caption("Racer")      # set window title

# load background image from file
background = pygame.image.load("photo/wall.png")

# scale background image to fit screen size
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# positions of two background images for scrolling effect
bg_y1 = 0                                # first background starts at top
bg_y2 = -SCREEN_HEIGHT                   # second background starts above screen

# load coin collection sound
coin_sound = pygame.mixer.Sound("sounds/gc.mp3")

# load crash sound
crash_sound = pygame.mixer.Sound("sounds/crash.mp3")

# load background music file
pygame.mixer.music.load("sounds/music.mp3")

# set background music volume
pygame.mixer.music.set_volume(0.3)

# play music infinitely (-1 means loop forever)
pygame.mixer.music.play(-1)

# create small font for score text
font_small = pygame.font.SysFont("Verdana", 20)

# create big font for game over text
font_big = pygame.font.SysFont("Verdana", 60)


# define player class (car controlled by user)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()               # initialize sprite parent class

        # load enemy image to reuse for player
        img = pygame.image.load("photo/enemy.png").convert_alpha()

        # get bounding rectangle of non-transparent pixels
        rect = img.get_bounding_rect()

        # crop image to remove empty transparent space
        img = img.subsurface(rect).copy()

        # recolor image using multiply blend mode to make it red
        img.fill((255, 0, 0), special_flags=pygame.BLEND_RGB_MULT)

        # rotate image so it faces upward (same direction as enemies)
        img = pygame.transform.rotate(img, 180)

        # resize image to standard size
        self.image = pygame.transform.scale(img, (50, 70))

        # create rectangle for position and set initial position
        self.rect = self.image.get_rect(center=(300, 330))

    def move(self):
        pressed_keys = pygame.key.get_pressed()   # get currently pressed keys

        # move left if left key is pressed and not outside screen
        if pressed_keys[K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-5, 0)

        # move right if right key is pressed and not outside screen
        if pressed_keys[K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.move_ip(5, 0)


# define coin class
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # load coin image with transparency
        img = pygame.image.load("photo/coin.png").convert_alpha()

        # scale coin to smaller size
        self.image = pygame.transform.scale(img, (30, 30))

        # spawn coin at random x position at top of screen
        self.rect = self.image.get_rect(center=(random.randint(20, 580), 0))

    def move(self):
        # move coin downward
        self.rect.move_ip(0, 5)

        # if coin goes below screen, remove it from game
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


# define enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # load enemy car image
        img = pygame.image.load("photo/enemy.png").convert_alpha()

        # crop empty transparent space
        rect = img.get_bounding_rect()
        img = img.subsurface(rect).copy()

        # rotate enemy so it moves toward player
        img = pygame.transform.rotate(img, 180)

        # resize enemy
        self.image = pygame.transform.scale(img, (50, 70))

        # spawn enemy at random x position at top
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, 560), 0)

    def move(self):
        # move enemy downward based on speed
        self.rect.move_ip(0, SPEED)

        # remove enemy if it goes off screen
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


# create player object
P1 = Player()

# create groups to store sprites
coins = pygame.sprite.Group()            # group for coins
enemies = pygame.sprite.Group()          # group for enemies
all_sprites = pygame.sprite.Group()      # group for all objects

# add player to sprite group
all_sprites.add(P1)

# create custom events for spawning objects
ADDCOIN = pygame.USEREVENT + 1           # unique event id for coin
ADDENEMY = pygame.USEREVENT + 2          # unique event id for enemy

# set timers to trigger events repeatedly
pygame.time.set_timer(ADDCOIN, 1200)     # spawn coin every 1200 ms
pygame.time.set_timer(ADDENEMY, 2000)    # spawn enemy every 2000 ms


# main game loop
while True:

    # process all events (keyboard, quit, timers)
    for event in pygame.event.get():

        # close window event
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # spawn coin when timer event triggers
        if event.type == ADDCOIN:
            coin = Coin()
            coins.add(coin)
            all_sprites.add(coin)

        # spawn enemy when timer event triggers
        if event.type == ADDENEMY:
            enemy = Enemy()
            enemies.add(enemy)
            all_sprites.add(enemy)

    # move both background images downward
    bg_y1 += SPEED
    bg_y2 += SPEED

    # reset position when background leaves screen
    if bg_y1 >= SCREEN_HEIGHT:
        bg_y1 = -SCREEN_HEIGHT

    if bg_y2 >= SCREEN_HEIGHT:
        bg_y2 = -SCREEN_HEIGHT

    # draw backgrounds
    screen.blit(background, (0, bg_y1))
    screen.blit(background, (0, bg_y2))

    # draw and update all sprites
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)
        entity.move()

    # check collision between player and coins
    for coin in coins:
        if pygame.sprite.collide_rect(P1, coin):
            coin_sound.play()            # play coin sound
            SCORE += 1                  # increase score
            coin.kill()                # remove coin

    # check collision between player and enemies
    if pygame.sprite.spritecollideany(P1, enemies):
        crash_sound.play()              # play crash sound
        time.sleep(1)                  # pause

        # draw red screen
        screen.fill((255, 0, 0))

        # render game over text
        text = font_big.render("GAME OVER", True, (0, 0, 0))
        screen.blit(text, (120, 150))

        pygame.display.update()        # update screen
        time.sleep(2)                 # show for 2 seconds

        pygame.quit()                 # exit game
        sys.exit()

    # draw white rectangle behind score text
    pygame.draw.rect(screen, (255,255,255), (430, 0, 170, 40))

    # render score text
    score_text = font_small.render("Coins: " + str(SCORE), True, (0,0,0))

    # draw score text
    screen.blit(score_text, (440, 5))

    pygame.display.update()           # update display

    pygame.time.Clock().tick(60)      # limit game to 60 FPS