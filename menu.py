"""
Importing important libraries
"""
from pygame.locals import *
import pygame
import sys
import main

"""
Setting up an environment to initialize pygame
"""
mainClock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption('game base')
screen = pygame.display.set_mode((1000, 600), 0, 32)

# setting font settings
font = pygame.font.SysFont(None, 30)

"""
A function that can be used to write text on our screen and buttons
"""


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


# A variable to check for the status later
click = False

# load background image
bg_image = pygame.image.load(
    "assets/images/background/background.jpg").convert_alpha()


def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (1000, 600))
    screen.blit(scaled_bg, (0, 0))

# Main container function that holds the buttons and game functions


def main_menu():
    while True:

        draw_bg()
        draw_text('Main Menu', font, (255, 255, 255), screen, 450, 200)

        mx, my = pygame.mouse.get_pos()

        # creating buttons
        button_1 = pygame.Rect(400, 260, 200, 50)
        button_2 = pygame.Rect(400, 340, 200, 50)

        # defining functions when a certain button is pressed
        if button_1.collidepoint((mx, my)):
            if click:
                game()
        if button_2.collidepoint((mx, my)):
            if click:
                options()
        pygame.draw.rect(screen, (153, 186, 221), button_1)
        pygame.draw.rect(screen, (153, 186, 221), button_2)

        # writing text on top of button
        draw_text('PLAY', font, (255, 255, 255), screen, 475, 275)
        draw_text('OPTIONS', font, (255, 255, 255), screen, 455, 355)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)


"""
This function is called when the "PLAY" button is clicked.
"""


def game():
    running = True
    while running:

        main.start_game()

        running = False
        pygame.display.update()
        mainClock.tick(60)


"""
This function is called when the "OPTIONS" button is clicked.
"""


def options():
    running = True
    while running:
        screen.fill((0, 0, 0))

        draw_text('OPTIONS SCREEN', font, (255, 255, 255), screen, 20, 20)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        pygame.display.update()
        mainClock.tick(60)


main_menu()
