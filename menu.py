import main

import pygame

from pygame.locals import *

import sys

# initialize pygame
mainClock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption('ZoinksKombat')
screen = pygame.display.set_mode((1000, 600), 0, 32)
font = pygame.font.SysFont(None, 30)
bg_image = pygame.image.load(
	"assets/images/background/background.jpg").convert_alpha()

def draw_text(text, font, color, surface, x, y):
	textobj = font.render(text, 1, color)
	textrect = textobj.get_rect()
	textrect.topleft = (x, y)
	surface.blit(textobj, textrect)

def draw_bg():
	scaled_bg = pygame.transform.scale(bg_image, (1000, 600))
	screen.blit(scaled_bg, (0, 0))

# function that contains the buttons and game functions
def main_menu(rounds):
	click = False

	while True:
		draw_bg()
		draw_text('Main Menu', font, (255, 255, 255), screen, 450, 200)
		mx, my = pygame.mouse.get_pos()

		# create buttons
		button_1 = pygame.Rect(400, 260, 200, 50)
		button_2 = pygame.Rect(400, 340, 200, 50)
		button_3 = pygame.Rect(400, 420, 200, 50)

		# define actions on click
		if button_1.collidepoint((mx, my)):
			if click:
				game(rounds)

		if button_2.collidepoint((mx, my)):
			if click:
				options(rounds)

		if button_3.collidepoint((mx, my)):
			if click:
				pygame.quit()
				exit()

		pygame.draw.rect(screen, (153, 186, 221), button_1)
		pygame.draw.rect(screen, (153, 186, 221), button_2)
		pygame.draw.rect(screen, (153, 186, 221), button_3)

		# write text to identify buttons
		draw_text('PLAY', font, (255, 255, 255), screen, 475, 275)
		draw_text('OPTIONS', font, (255, 255, 255), screen, 455, 355)
		draw_text('QUIT', font, (255, 255, 255), screen, 475, 435)

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


# action run when clicked on "PLAY"
def game(rounds):
	running = True

	while running:
		winner = main.start_game(rounds)
		winner_screen(winner)
		running = False
		pygame.display.update()
		mainClock.tick(60)

def winner_screen(winner):
	running = True
	click = False

	while running:
		draw_bg()
        mx, my = pygame.mouse.get_pos()
		
		if (winner == 0):
			draw_text('P1 WINS!', font, (0, 255, 0), screen, 440, 150)
		else:
			draw_text('P2 WINS...', font, (255, 0, 0), screen, 440, 150)

		# create buttons
		button_1 = pygame.Rect(385, 260, 200, 50)
		button_2 = pygame.Rect(385, 340, 200, 50)

		# define actions on click
		if button_1.collidepoint((mx, my)):
			if click:
				main_menu(2)

		if button_2.collidepoint((mx, my)):
			if click:
				pygame.quit()
				sys.exit()

		pygame.draw.rect(screen, (153, 186, 221), button_1)
		pygame.draw.rect(screen, (153, 186, 221), button_2)

		# write text to identify buttons
		draw_text('MENU', font, (255, 255, 255), screen, 458, 275)
		draw_text('QUIT', font, (255, 255, 255), screen, 460, 355)

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

# action run when clicked on "OPTIONS"
def options(rounds):
	running = True
	click = False

	while running:
		draw_bg()
		draw_text('LIKE ZOINKS SCOOB, THIS IS ONE OF THOSE OPTION SELECT THINGIES!', font, (0, 255, 0), screen, 20, 20)
        mx, my = pygame.mouse.get_pos()
		
		if (rounds != -1):
			draw_text('I SHALL MAKE QUICK WORK OF YOU...', font, (255, 0, 0), screen, 20, 60)
		else:
			draw_text('IF AN ETERNAL SUFFERING IS WHAT YOU DESIRE, THEN SO BE IT...', font, (255, 0, 0), screen, 20, 60)

		# create buttons
		button_1 = pygame.Rect(400, 260, 200, 50)
		button_2 = pygame.Rect(400, 340, 200, 50)
		button_3 = pygame.Rect(400, 420, 200, 50)

		# define actions on click
		if button_1.collidepoint((mx, my)):
			if click:
				main_menu(2)

		if button_2.collidepoint((mx, my)):
			if click:
				main_menu(-1)

		if button_3.collidepoint((mx, my)):
			if click:
				main_menu(rounds)

		pygame.draw.rect(screen, (153, 186, 221), button_1)
		pygame.draw.rect(screen, (153, 186, 221), button_2)
		pygame.draw.rect(screen, (153, 186, 221), button_3)

		# write text to identify buttons
		draw_text('CLASSIC', font, (255, 255, 255), screen, 460, 275)
		draw_text('UNLIMITED', font, (255, 255, 255), screen, 450, 355)
		draw_text('BACK', font, (255, 255, 255), screen, 475, 435)

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

main_menu(2)
