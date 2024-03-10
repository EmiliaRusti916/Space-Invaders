import math
import random

import pygame
from pygame import mixer

pygame.init()
pygame.font.init()

player_image = pygame.image.load('spaceship.png')
missile_image = pygame.image.load('rocket-ship-launch.png')
collision_image = pygame.image.load('explosion.png')

font = pygame.font.Font('freesansbold.ttf', 32)
over_font = pygame.font.Font('freesansbold.ttf', 64)
win_font = pygame.font.Font('freesansbold.ttf', 64)
text_x = 25
text_y = 550

player_y = 450
player_x = 370
x_coordinate_change = 0

invader_image = []
invader_x = []
invader_y = []
x_invader_change = []
y_invader_change = []

number_of_invaders = 6

for i in range(number_of_invaders):
    invader_image.append(pygame.image.load('invader.png'))
    invader_x.append(random.randint(0, 734))
    invader_y.append(random.randint(10, 200))
    x_invader_change.append(1.5)
    y_invader_change.append(25)

missile_x = 0
missile_y = 450
x_missile_change = 0
y_missile_change = 3
missile_status = 'ready'
# status can be ready (not seen on screen) or fired (seen on screen)

score_value = 0
collision = 0

screen = pygame.display.set_mode((800, 600))
background = pygame.image.load('background.jpg')
pygame.display.set_caption('Space Invaders')
mixer.music.load('background_sound.mp3')
mixer.music.play(-1)
# https://www.flaticon.com/free-icon/spaceship_1985789?term=spaceship&page=1&position=4&origin=search&related_id=1985789
# <a href="https://www.flaticon.com/free-icons/spaceship"
# title="spaceship icons">Spaceship icons created by Wendy-G - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/explosion" title="explosion icons">Explosion icons created by Smashicons
# - Flaticon</a>
pygame.display.set_icon(pygame.image.load('001-spaceship.png'))


def set_player(x, y):
    screen.blit(player_image, (x, y))


def show_score(x, y):
    score = font.render('Score: ' + str(score_value) + '/5000', True, (204, 229, 255))
    screen.blit(score, (x, y))


def set_invader(x, y, i):
    screen.blit(invader_image[i], (x, y))


def fire_bullet(x, y):
    global missile_status
    missile_status = 'fired'
    screen.blit(missile_image, (x + 16, y + 5))


def invader_shot(inv_x, inv_y, miss_x, miss_y):
    distance = math.sqrt(math.pow(inv_x - miss_x, 2) + math.pow(inv_y - miss_y, 2))
    if distance < 27:
        return True
    return False


def shot(x, y, i):
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < 60:
        screen.blit(collision_image, (x, y))
        set_player(player_x, player_y)
        pygame.display.update()
        for inv in range(number_of_invaders):
            if inv != i:
                set_invader(invader_x[inv], invader_y[inv], inv)
        clock.tick(60)


def game_over():
    over = over_font.render('Game Over', True, (204, 229, 255))
    screen.blit(over, (225, 275))


def completed():
    win = win_font.render('Game Completed', True, (204, 229, 255))
    screen.blit(win, (150, 275))


while True:
    # RBG Red Green Blue
    screen.fill((0, 0, 25))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                x_coordinate_change = -1
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                x_coordinate_change = 1
            if event.key == pygame.K_SPACE:
                if missile_status == 'ready':
                    missile_sound = mixer.Sound('laser.wav')
                    missile_sound.play()
                    missile_x = player_x
                    fire_bullet(missile_x, missile_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or \
                    event.key == pygame.K_d:
                x_coordinate_change = 0

    player_x += x_coordinate_change
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    for i in range(number_of_invaders):

        if score_value < 5000 and invader_y[i] > 420:
            for j in range(number_of_invaders):
                invader_y[j] = 2000
            game_over()
            break
        invader_x[i] += x_invader_change[i]

        if invader_x[i] <= 0:
            x_invader_change[i] = 0.75
            invader_y[i] += y_invader_change[i]

        elif invader_x[i] >= 736:
            x_invader_change[i] = -0.75
            invader_y[i] += y_invader_change[i]

        if invader_shot(invader_x[i], invader_y[i], missile_x, missile_y) is True:
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            invader_x[i] = random.randint(0, 734)
            invader_y[i] = random.randint(10, 150)
            shot(missile_x, missile_y, i)
            missile_y = 450
            missile_status = 'ready'
            score_value += 100
        set_invader(invader_x[i], invader_y[i], i)

    if score_value == 5000:
        completed()
        for j in range(number_of_invaders):
            invader_y[j] = 2000

    if missile_status == 'fired':
        fire_bullet(missile_x, missile_y)
        missile_y -= y_missile_change

    if missile_y <= 0:
        missile_y = 450
        missile_status = 'ready'

    set_player(player_x, player_y)
    show_score(text_x, text_y)
    pygame.display.update()
