import pygame
import random
from player import Player
from pygame.locals import (K_RETURN, K_UP, K_LEFT, K_RIGHT, K_DOWN, K_SPACE)
import time

time_lapsed = 0


pygame.init()

font_obj = pygame.font.SysFont(None, 100, 0, 0)
you_lose = font_obj.render("You Died...", True, (250, 0, 0))
you_win = font_obj.render("You Win! Your time was", True, (0, 250, 0))
try_again = font_obj.render("Press Enter To Try Again", True, (250, 0, 0))

clock = pygame.time.Clock()
minutes = 0
seconds = 0
milliseconds = 0

PIXEL_DIM = 40

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800

block_map = {}


# the input for different blocks
class Block(pygame.sprite.Sprite):

    def __init__(self, name, width, height):
        if name == "water":
            color = (0, 0, 255 - random.randint(0, 100))
        if name == "grass":
            color = (127, 255 - random.randint(0, 40), 127)
        if name == "win":
            color = (0, 0 + random.randint(0, 40), 0)
        self.name = name
        self.image = pygame.Surface([width, height])
        self.image.fill(color)


# generates the blocks
def add_block(x, y):
    global block_map, name
    block_type = random.randint(0, 10000)
    if block_type in range(2001, 9998):
        name = "grass"
    if block_type in range(1, 2000):
        name = "water"
    if block_type == 9999:
        name = "win"
    block_map[(x, y)] = Block(name, PIXEL_DIM, PIXEL_DIM)


# initialize map
# determine how many blocks will need to be generated
# based on PIXEL_DIM and SCREEN_HEIGHT and SCREEN_WIDTH
# and generate each needed block
for i in range(int(SCREEN_WIDTH / PIXEL_DIM) + 2):
    for j in range(int(SCREEN_HEIGHT / PIXEL_DIM) + 2):
        add_block(i, j)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
lose_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
win_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
oversize = pygame.Surface((SCREEN_WIDTH + PIXEL_DIM * 2, SCREEN_HEIGHT + PIXEL_DIM * 2))
gameExit = False


class Health_bar():
    def __init__(self):
        self.level = 10
        self.heart = pygame.transform.scale(pygame.image.load("heart.png").convert_alpha(), (20, 20))
        self.whb = pygame.Surface((200, 20), pygame.SRCALPHA, 32).convert_alpha()
        for hearts in range(self.level):
            self.whb.blit(self.heart, (hearts * 20, 0))

    def set_level(self, new_level):
        self.level = new_level
        self.whb = pygame.Surface((200, 20), pygame.SRCALPHA, 32).convert_alpha()
        for hearts in range(self.level):
            self.whb.blit(self.heart, (hearts * 20, 0))


frame_count = 0


def is_allowed(key):
    cbx = int(x + (SCREEN_WIDTH / PIXEL_DIM + 2) / 2) - 1
    cby = int(y + int((SCREEN_HEIGHT / PIXEL_DIM + 2) / 2))
    # if block_map[(cbx + 1,cby)].name == "water" and key == K_RIGHT and xo > 15:

    return True


def drown():
    cbx = int(x + (SCREEN_WIDTH / PIXEL_DIM + 2) / 2) - 1
    cby = int(y + int((SCREEN_HEIGHT / PIXEL_DIM + 2) / 2))
    if block_map[(cbx, cby)].name == "water":
        return True


def win():
    cbx = int(x + (SCREEN_WIDTH / PIXEL_DIM + 2) / 2) - 1
    cby = int(y + int((SCREEN_HEIGHT / PIXEL_DIM + 2) / 2))
    if block_map[(cbx, cby)].name == "win":

        return True


frame_count = 0
x = 0
y = 0

xo = 0
yo = 0

speed = 5


def cam_scroll(key_pressed):
    global xo, yo, x, y, player
    if key_pressed[K_LEFT] and is_allowed(K_LEFT):
        xo += speed
        player.face("left")
        if xo > PIXEL_DIM:
            xo = 0
            x -= 1
    if key_pressed[K_RIGHT] and is_allowed(K_RIGHT):
        xo -= speed
        player.face("right")
        if xo < 0:
            x += 1
            xo += PIXEL_DIM
    if key_pressed[K_UP] and is_allowed(K_UP):
        yo += speed
        player.face("up")
        if yo > PIXEL_DIM:
            y -= 1
            yo = 0
    if key_pressed[K_DOWN] and is_allowed(K_DOWN):
        yo -= speed
        player.face("down")
        if yo < 0:
            y += 1
            yo += PIXEL_DIM


def prepare_map():
    global x, y
    for i in range(x, x + int(SCREEN_WIDTH / PIXEL_DIM) + 2):
        for j in range(y, y + int(SCREEN_HEIGHT / PIXEL_DIM) + 2):
            if (i, j) not in block_map:
                add_block(i, j)
lose_game = False
win_game = False

player = Player(PIXEL_DIM, PIXEL_DIM)
clock = pygame.time.Clock()
player_health_bar = Health_bar()

def lose():
    while True:
        screen.fill((250,0,0))
        screen.blit(you_lose, (300,400))
while not gameExit:
    if player_health_bar.level < 1:
        lose_game = True
        gameExit = True
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True
    start_time = time.time()
    clock.tick(80)
    key_pressed = pygame.key.get_pressed()
    cam_scroll(key_pressed)
    prepare_map()
    drown()
    win()

    if frame_count % 20 == 0:
        if drown():
            player_health_bar.set_level(player_health_bar.level - 1)

    if win():
        screen.blit(you_win, (22, 0))
        screen.blit(timelabel, (22, 10))
        break
    frame_count += 1

    for i in range(int(SCREEN_WIDTH / PIXEL_DIM) + 2):
        for j in range(int(SCREEN_HEIGHT / PIXEL_DIM) + 2):
            oversize.blit(block_map[(x + i, y + j)].image, (PIXEL_DIM * i, PIXEL_DIM * j))
        print(f'x:{x + (SCREEN_WIDTH / PIXEL_DIM + 2) / 2}, xo:{xo}, y:{y + (SCREEN_HEIGHT / PIXEL_DIM + 2) / 2}, yo:{yo}, block:{block_map[int(x + (SCREEN_WIDTH / PIXEL_DIM + 2) / 2) - 1, y + int((SCREEN_HEIGHT / PIXEL_DIM + 2) / 2)].name}')
    oversize.scroll(xo, yo)
    screen.blit(oversize, (-PIXEL_DIM, -PIXEL_DIM))
    screen.blit(player.image, (SCREEN_WIDTH / 2 - PIXEL_DIM / 2, SCREEN_HEIGHT / 2 - PIXEL_DIM / 2))
    screen.blit(player_health_bar.whb, (0, 0))

    if milliseconds > 1000:
        seconds += 1
        milliseconds -= 1000
        screen.blit(screen, (0, 0))
        pygame.display.update()

    if seconds > 60:
        minutes += 1
        seconds -= 60
    milliseconds += clock.tick_busy_loop(60)
    timelabel = font_obj.render("{}:{}".format(minutes, seconds), True, (0, 0, 0))
    screen.blit(timelabel, (700, 2))

    pygame.display.update()
while gameExit:
    print("1")
    if lose_game:
        print("2")
        screen.fill((0,0,0))
        screen.blit(you_lose, (100,250))
        #screen.blit(try_again, (100,350))
        pygame.display.update()
        print("3")
    if event.type == pygame.KEYDOWN:
        print("4")
        if event.key == pygame.K_ENTER:
            print("5")
            minutes = 0
            seconds = 0
            milliseconds = 0
            block_map = {}
            prepare_map()
            gameExit = False
