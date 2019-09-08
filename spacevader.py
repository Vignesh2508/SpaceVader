import pygame
import sys
import random

import time

pygame.init()

WIDTH = 800
HEIGHT = 600

RED = (255,0,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
WHITE = (255,255,255)

SPEED = 10

BGROUND_COLOR = (0,0,0)

score = 0

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SpaceVader")

game_over = False

clock = pygame.time.Clock()

myFont = pygame.font.SysFont("monospace", 35)

bg_img = pygame.image.load('starfield.png')

vehicle = pygame.image.load('spacevader.png')

icon = pygame.image.load('spacevader_icon.png')

pygame.display.set_icon(icon)

meteor = pygame.image.load('meteor.png')

player_width = vehicle.get_width()
enemy_width = meteor.get_width()

player_height = vehicle.get_height()
enemy_height = meteor.get_height()

player_height = player_width = enemy_height = enemy_width = 50

player_pos = [WIDTH/2,HEIGHT-2*player_height]

enemy_pos = [random.randint(0,WIDTH-enemy_width),0]

enemy_list = [enemy_pos]


def text_objects(text, font):
    textsurface = font.render(text, True, WHITE)
    return textsurface,textsurface.get_rect()

def message_display(text):
    largetext = pygame.font.Font("freesansbold.ttf",80)
    textsurf, textrect = text_objects(text, largetext)
    textrect.center=((WIDTH/2),(HEIGHT/2))
    screen.blit(textsurf,textrect)
    pygame.display.update()
    time.sleep(3)

def crash():
    message_display("YOU CRASHED")

def drop_enemies(enemy_list):
    delay = random.random()
    if len(enemy_list) < 10 and delay < 0.1:
        x_pos = random.randint(0, WIDTH-enemy_width)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])

def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
        #pygame.draw.rect(screen, BLUE, (enemy_pos[0], enemy_pos[1], enemy_width, enemy_height))
        screen.blit(meteor, (enemy_pos[0], enemy_pos[1]))

def update_enemies(enemy_list, score):
    for idx, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1] >= 0 and enemy_pos[1] < HEIGHT:
            enemy_pos[1] += SPEED
        else:
            enemy_list.pop(idx)
            score += 1
    return score

def collision_check(enemy_list, player_pos):
    for enemy_pos in enemy_list:
        if detect_collision(enemy_pos, player_pos):
            return True
    return False

def detect_collision(player_pos, enemy_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    e_x = enemy_pos[0]
    e_y = enemy_pos[1]

    if (e_x >= p_x and e_x < (p_x + player_width)) or (p_x >= e_x and p_x < (e_x + enemy_width)):
        if (e_y >= p_y and e_y < (p_y + player_height)) or (p_y >= e_y and p_y < (e_y + enemy_height)):
            return True
    return False


while not game_over:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()

    if event.type == pygame.KEYDOWN:
        x = player_pos[0]
        y = player_pos[1]
        if event.key == pygame.K_LEFT:
            x-=10
        elif event.key == pygame.K_RIGHT:
            x+=10
        player_pos = [x,y]

    #screen.fill(BGROUND_COLOR)
    screen.blit(bg_img, bg_img.get_rect())

    if detect_collision(player_pos, enemy_pos):
        game_over = True
        break

    drop_enemies(enemy_list)
    score = update_enemies(enemy_list, score)

    text = "Score:" + str(score)
    label = myFont.render(text, 1, YELLOW)
    screen.blit(label, (WIDTH-200, HEIGHT-40))
    text1 = "Creator: vickky"
    label1 = myFont.render(text1, 1, YELLOW)
    screen.blit(label1, (0, HEIGHT-40))

    if collision_check(enemy_list, player_pos):
        crash()
        game_over = True
        break

    draw_enemies(enemy_list)
    #pygame.draw.rect(screen, RED, (player_pos[0], player_pos[1], player_width, player_height))
    screen.blit(vehicle, (player_pos[0],player_pos[1]))
    clock.tick(30)
    pygame.display.update()