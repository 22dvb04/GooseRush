import random
import os
import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

FPS = pygame.time.Clock()

HEIGHT = 800
WIDTH = 1280

FONT = pygame.font.SysFont('Verdana', 20)

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)
PLAYER_SIZE = (20, 20)
ENEMY_SIZE = (150, 50)
BONUS_SIZE = (80, 130)

main_display = pygame.display.set_mode((WIDTH, HEIGHT))

required_files = ['background.png', 'player.png', 'enemy.png', 'bonus.png']
for file in required_files:
    if not os.path.exists(file):
        raise FileNotFoundError(f"File '{file}' not find!")

bg = pygame.transform.scale(pygame.image.load('background.png'), (WIDTH, HEIGHT))
bg_X1 = 0
bg_X2 = bg.get_width()
bg_move = 3

IMAGE_PATH = "Goose"
PLAYER_IMAGES = os.listdir(IMAGE_PATH)

image_index = 0 

playing = True

player = pygame.image.load('player.png').convert_alpha()
player_rect = player.get_rect()
player_move_down = [0, 4]
player_move_up = [0, -4]
player_move_left = [-4, 0]
player_move_right = [4, 0]

def create_enemy():
    enemy = pygame.image.load('enemy.png')
    enemy = pygame.transform.scale(enemy, ENEMY_SIZE)
    enemy_rect = pygame.Rect(WIDTH, random.randint(0 + enemy.get_height(), HEIGHT - enemy.get_height()), *ENEMY_SIZE)
    enemy_speed = [random.randint(-8, -4), 0]
    return [enemy, enemy_rect, enemy_speed]

def create_bonus():
    bonus = pygame.image.load('bonus.png')
    bonus = pygame.transform.scale(bonus, BONUS_SIZE)
    bonus_rect = pygame.Rect(random.randint(0, WIDTH - BONUS_SIZE[0]), 0, *BONUS_SIZE)
    bonus_speed = random.randint(4, 8)
    return [bonus, bonus_rect, bonus_speed]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 3000)

CHANGE_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMAGE, 200)

enemies = []
bonuses = []
score = 0



while playing:
    FPS.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        if event.type == CHANGE_IMAGE:
            player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index]))
            image_index += 1
            if image_index >= len(PLAYER_IMAGES):
                image_index = 0

    bg_X1 -= bg_move
    bg_X2 -= bg_move

    if bg_X1 < -bg.get_width() :
        bg_X1 = bg.get_width()
    if bg_X2 < -bg.get_width() :
        bg_X2 = bg.get_width()

    main_display.blit(bg, (bg_X1, 0))
    main_display.blit(bg, (bg_X2, 0))

    keys = pygame.key.get_pressed()

    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(player_move_down)
    if keys[K_UP] and player_rect.top > 0:
        player_rect = player_rect.move(player_move_up)
    if keys[K_LEFT] and player_rect.left > 0:    
        player_rect = player_rect.move(player_move_left)
    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)

    for enemy in enemies:
        main_display.blit(enemy[0], enemy[1])
        enemy[1] = enemy[1].move(enemy[2])

        if player_rect.colliderect(enemy[1]):
            playing = False
            print('Game Over')

    for bonus in bonuses:
        main_display.blit(bonus[0], bonus[1])
        bonus[1] = bonus[1].move(0, bonus[2])

        if player_rect.colliderect(bonus[1]):
            score += 1
            bonuses.pop(bonuses.index(bonus))

    main_display.blit(FONT.render(f'Score: {score}', True, COLOR_BLACK), (20, 20))
    main_display.blit(player, player_rect)

    pygame.display.flip()
    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.remove(enemy)

    for bonus in bonuses:
        if bonus[1].top > HEIGHT:
            bonuses.pop(bonuses.index(bonus))


