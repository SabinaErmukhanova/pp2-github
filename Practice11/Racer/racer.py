import pygame, sys, random, time      # import libraries: pygame for game, sys for exit, random for spawning, time for delays
from pygame.locals import *           # import pygame constants like QUIT, K_LEFT, etc.

pygame.init()                         # initialize all pygame modules (graphics, events, etc.)
pygame.mixer.init()                  # initialize sound system

# ---------- SETTINGS ----------
SCREEN_WIDTH = 600                   # width of the game window
SCREEN_HEIGHT = 400                  # height of the game window
SPEED = 3                            # base speed (affects background, coins, enemies)
SCORE = 0                            # player score (coins collected)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))   # create window
pygame.display.set_caption("Racer")  # set window title

# ---------- BACKGROUND ----------
background = pygame.image.load("photo/road.png")   # load road image
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))  # scale to fit screen

bg_y1 = 0                         # first background position (starts on screen)
bg_y2 = -SCREEN_HEIGHT            # second background starts above screen (for scrolling effect)

# ---------- SOUNDS ----------
coin_sound = pygame.mixer.Sound("sound/gc.mp3")    # sound when collecting coin
crash_sound = pygame.mixer.Sound("sound/crash.mp3")# sound when crashing

pygame.mixer.music.load("sound/music.mp3")  # load background music
pygame.mixer.music.set_volume(0.3)          # set volume
pygame.mixer.music.play(-1)                 # play music in loop

# ---------- FONTS ----------
font_small = pygame.font.SysFont("Verdana", 20)   # small font for score
font_big = pygame.font.SysFont("Verdana", 60)     # big font for game over

# ---------- PLAYER ----------
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()   # initialize parent sprite class

        img = pygame.image.load("photo/Player.png").convert_alpha()   # load player image with transparency
        rect = img.get_bounding_rect()   # get bounding box (removes empty transparent space)
        img = img.subsurface(rect).copy()  # crop image

        # set player size (same height as enemy but wider)
        self.image = pygame.transform.scale(img, (90, 100))
        self.rect = self.image.get_rect(center=(300, 330))  # starting position

        self.rect.inflate_ip(-20, -20)   # shrink hitbox (collision area smaller than image)

    def move(self):
        keys = pygame.key.get_pressed()  # get pressed keys

        # move left if not outside screen
        if keys[K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-5, 0)

        # move right if not outside screen
        if keys[K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.move_ip(5, 0)

# ---------- COIN ----------
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # randomly choose coin value with probabilities
        self.value = random.choices([1, 2, 3], weights=[70, 20, 10])[0]

        # choose image and size based on value
        if self.value == 1:
            img = pygame.image.load("photo/coin.png").convert_alpha()
            size = 30
        elif self.value == 2:
            img = pygame.image.load("photo/diamond.png").convert_alpha()
            size = 35
        else:
            img = pygame.image.load("photo/rare.png").convert_alpha()
            size = 40

        self.image = pygame.transform.scale(img, (size, size))  # scale coin

        # spawn coin at random x position at top
        self.rect = self.image.get_rect(
            center=(random.randint(20, SCREEN_WIDTH - 20), 0)
        )

    def move(self):
        self.rect.move_ip(0, SPEED)   # move coin downward

        if self.rect.top > SCREEN_HEIGHT:  # if coin goes off screen
            self.kill()   # remove coin

# ---------- ENEMY ----------
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        img = pygame.image.load("photo/enemy.png").convert_alpha()  # load enemy image
        rect = img.get_bounding_rect()  # remove transparent borders
        img = img.subsurface(rect).copy()

        img = pygame.transform.rotate(img, 180)  # rotate to face player
        self.image = pygame.transform.scale(img, (50, 70))  # set size

        # spawn enemy at random x position at top
        self.rect = self.image.get_rect(
            center=(random.randint(40, SCREEN_WIDTH - 40), 0)
        )

        self.rect.inflate_ip(-20, -20)  # shrink collision box

    def move(self):
        self.rect.move_ip(0, SPEED + 1)  # move downward (slightly faster than background)

        if self.rect.top > SCREEN_HEIGHT:  # if enemy leaves screen
            self.kill()   # remove enemy

# ---------- GAME OVER ----------
def crash():
    crash_sound.play()  # play crash sound
    time.sleep(1)       # short pause

    screen.fill((255, 0, 0))  # red screen
    text = font_big.render("GAME OVER", True, (0, 0, 0))  # render text
    screen.blit(text, (120, 150))

    pygame.display.update()  # update screen
    time.sleep(2)            # show for 2 seconds

    pygame.quit()            # close game
    sys.exit()

# ---------- OBJECTS ----------
P1 = Player()   # create player

coins = pygame.sprite.Group()    # group for coins
enemies = pygame.sprite.Group()  # group for enemies
all_sprites = pygame.sprite.Group()  # group for everything

all_sprites.add(P1)  # add player to group

# ---------- EVENTS ----------
ADDCOIN = pygame.USEREVENT + 1   # custom event for spawning coin
ADDENEMY = pygame.USEREVENT + 2  # custom event for spawning enemy

pygame.time.set_timer(ADDCOIN, 1200)   # spawn coin every 1.2 seconds
pygame.time.set_timer(ADDENEMY, 2000)  # spawn enemy every 2 seconds

# ---------- GAME LOOP ----------
while True:

    for event in pygame.event.get():  # process events
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # spawn coin
        if event.type == ADDCOIN:
            c = Coin()
            coins.add(c)
            all_sprites.add(c)

        # spawn enemy
        if event.type == ADDENEMY:
            e = Enemy()
            enemies.add(e)
            all_sprites.add(e)

    # ---------- BACKGROUND ----------
    bg_y1 += SPEED   # move first background down
    bg_y2 += SPEED   # move second background down

    # reset backgrounds when they leave screen
    if bg_y1 >= SCREEN_HEIGHT:
        bg_y1 = -SCREEN_HEIGHT
    if bg_y2 >= SCREEN_HEIGHT:
        bg_y2 = -SCREEN_HEIGHT

    screen.blit(background, (0, bg_y1))  # draw first background
    screen.blit(background, (0, bg_y2))  # draw second background

    # ---------- DRAW ----------
    for entity in all_sprites:   # draw and update all objects
        screen.blit(entity.image, entity.rect)
        entity.move()

    # ---------- COINS ----------
    for coin in coins:
        if pygame.sprite.collide_rect(P1, coin):  # collision with player
            coin_sound.play()
            SCORE += coin.value  # add score based on coin type
            coin.kill()          # remove coin

            # increase speed every 10 coins
            if SCORE % 10 == 0 and SCORE != 0:
                SPEED += 1

    # ---------- ENEMY ----------
    if pygame.sprite.spritecollideany(P1, enemies):  # collision with enemy
        crash()

    # ---------- SCORE ----------
    pygame.draw.rect(screen, (255,255,255), (430, 0, 170, 40))  # background for text
    score_text = font_small.render("Coins: " + str(SCORE), True, (0,0,0))
    screen.blit(score_text, (440, 5))  # draw score

    pygame.display.update()  # update screen

    pygame.time.Clock().tick(60)  # limit to 60 FPS