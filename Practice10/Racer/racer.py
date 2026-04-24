import pygame, sys, random, time
from pygame.locals import *

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
SPEED = 5
SCORE = 0

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer")

background = pygame.image.load("photo/wall.png")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

coin_sound = pygame.mixer.Sound("sounds/gc.mp3")
crash_sound = pygame.mixer.Sound("sounds/crash.mp3")

pygame.mixer.music.load("sounds/music.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

font_small = pygame.font.SysFont("Verdana", 20)
font_big = pygame.font.SysFont("Verdana", 60)

#  PLAYER 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #img = pygame.image.load("photo/Player.png").convert_alpha()
        img = pygame.image.load("photo/Player.png").convert()
        img.set_colorkey((255, 255, 255))  # убираем белый цвет
        

        rect = img.get_bounding_rect()
        img = img.subsurface(rect).copy()
        img = img.subsurface((5, 5, rect.width - 10, rect.height - 10)).copy()

        img = pygame.transform.rotate(img, 180)
        self.image = pygame.transform.scale(img, (50, 70))

        self.rect = self.image.get_rect(center=(300, 330))

    def move(self):
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-5, 0)

        if pressed_keys[K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.move_ip(5, 0)

#  COIN 
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        img = pygame.image.load("photo/coin.png").convert_alpha()
        self.image = pygame.transform.scale(img, (30, 30))
        self.rect = self.image.get_rect(center=(random.randint(20, 580), 0))

    def move(self):
        self.rect.move_ip(0, 5)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

#  ENEMY 
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        img = pygame.image.load("photo/enemy.png").convert_alpha()

        rect = img.get_bounding_rect()
        img = img.subsurface(rect).copy()

        img = pygame.transform.rotate(img, 180)
        self.image = pygame.transform.scale(img, (50, 70))

        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, 560), 0)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

P1 = Player()

coins = pygame.sprite.Group()
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

all_sprites.add(P1)

ADDCOIN = pygame.USEREVENT + 1
ADDENEMY = pygame.USEREVENT + 2

pygame.time.set_timer(ADDCOIN, 1200)
pygame.time.set_timer(ADDENEMY, 2000)

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == ADDCOIN:
            coin = Coin()
            coins.add(coin)
            all_sprites.add(coin)

        if event.type == ADDENEMY:
            enemy = Enemy()
            enemies.add(enemy)
            all_sprites.add(enemy)

    screen.blit(background, (0, 0))

    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)
        entity.move()

    # COINS 
    for coin in coins:
        if pygame.sprite.collide_rect(P1, coin):
            coin_sound.play()
            SCORE += 1
            coin.kill()

    #  GAME OVER 
    if pygame.sprite.spritecollideany(P1, enemies):
        crash_sound.play()
        time.sleep(1)

        screen.fill((255, 0, 0))
        text = font_big.render("GAME OVER", True, (0, 0, 0))
        screen.blit(text, (120, 150))

        pygame.display.update()
        time.sleep(2)

        pygame.quit()
        sys.exit()

    #  SCORE DISPLAY 
    pygame.draw.rect(screen, (255,255,255), (430, 0, 170, 40))  # фон под текст
    score_text = font_small.render("Coins: " + str(SCORE), True, (0,0,0))
    screen.blit(score_text, (440, 5))

    pygame.display.update()
    pygame.time.Clock().tick(60)