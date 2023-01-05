import pygame

from pygame import mixer

from fighter import Fighter

def start_game(rounds):
	mixer.init()
	pygame.font.init()

	# set window dimensions
	SCREEN_WIDTH = 1000
	SCREEN_HEIGHT = 600
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	pygame.display.set_caption("ZoinksKombat")

    # used colours
	RED = (255, 0, 0)
	GREEN = (0, 255, 0)
	WHITE = (255, 255, 255)

	# set framerate
    FPS = 60
	clock = pygame.time.Clock()

    # fighters variables
	SHAGGY_SIZE = 100
	SHAGGY_SCALE = 4
	SHAGGY_OFFSET = [50, 23]
	HORSEMAN_SIZE = 100
	HORSEMAN_SCALE = 4
	HORSEMAN_OFFSET = [50, 23]

	# game variables
	intro_count = 3
	last_count_update = pygame.time.get_ticks()
	round_over = False
	ROUND_OVER_COOLDOWN = 2000

    # players score
    score = [0, 0]

    # load images
	bg_image = pygame.image.load(
		"assets/images/background/background.jpg").convert_alpha()
	victory_img = pygame.image.load(
		"assets/images/icons/victory.png").convert_alpha()

    # load spritesheets
	SHAGGY_sheet = pygame.image.load(
		"assets/images/shaggy/Sprites/shaggy.png").convert_alpha()
	HORSEMAN_sheet = pygame.image.load(
		"assets/images/horseman/Sprites/horseman.png").convert_alpha()

	# load music and SFX
	pygame.mixer.music.load("assets/audio/song.mp3")
	pygame.mixer.music.set_volume(0.5)
	pygame.mixer.music.play(-1, 0.0, 0)
	punch_fx = pygame.mixer.Sound("assets/audio/punch.mp3")
	punch_fx.set_volume(0.5)
	sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
	sword_fx.set_volume(0.5)
	magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
	magic_fx.set_volume(0.75)

    # set fonts
    score_font = pygame.font.Font("assets/fonts/comic.TTF", 30)
	count_font = pygame.font.Font("assets/fonts/comic.TTF", 80)

	# set steps count for each animation
	SHAGGY_ANIMATION_STEPS = [6, 5, 3, 6, 3, 2, 3]
	HORSEMAN_ANIMATION_STEPS = [3, 3, 1, 6, 6, 2, 5]

	def draw_text(text, font, text_col, x, y):
		img = font.render(text, True, text_col)
		screen.blit(img, (x, y))

	def draw_bg():
		scaled_bg = pygame.transform.scale(
			bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
		screen.blit(scaled_bg, (0, 0))

	def draw_health_bar(health, x, y):
		ratio = health / 100
		pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
		pygame.draw.rect(screen, RED, (x, y, 400, 30))
		pygame.draw.rect(screen, GREEN, (x, y, 400 * ratio, 30))

	# create two Fighter objects
	fighter_1 = Fighter(1, 200, 310, False, SHAGGY_SIZE, SHAGGY_SCALE, SHAGGY_OFFSET,
						SHAGGY_sheet, SHAGGY_ANIMATION_STEPS, [punch_fx, punch_fx])
	fighter_2 = Fighter(2, 700, 310, True, HORSEMAN_SIZE, HORSEMAN_SCALE, HORSEMAN_OFFSET,
						HORSEMAN_sheet, HORSEMAN_ANIMATION_STEPS, [sword_fx, magic_fx])

	# running game loop
	run = True
	while run:
		clock.tick(FPS)
		draw_bg()

		# display player stats
		draw_health_bar(fighter_1.health, 20, 20)
		draw_health_bar(fighter_2.health, 580, 20)
		draw_text("P1: " + str(score[0]), score_font, RED, 20, 60)
		draw_text("P2: " + str(score[1]), score_font, RED, 580, 60)

		# countdown updater
		if intro_count <= 0:
			fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT,
						   screen, fighter_2, round_over)
			fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT,
						   screen, fighter_1, round_over)
		else:
			# show timer
			draw_text(str(intro_count), count_font, RED,
					  SCREEN_WIDTH / 2 - 20, SCREEN_HEIGHT / 3)
			# update timer
			if (pygame.time.get_ticks() - last_count_update) >= 1000:
				intro_count -= 1
				last_count_update = pygame.time.get_ticks()

		fighter_1.update()
		fighter_2.update()

		fighter_1.draw(screen)
		fighter_2.draw(screen)

		# check final result for current round
		if round_over == False:
			if fighter_1.alive == False:
				score[1] += 1
				round_over = True
				round_over_time = pygame.time.get_ticks()
			elif fighter_2.alive == False:
				score[0] += 1
				round_over = True
				round_over_time = pygame.time.get_ticks()
		else:
			if (rounds != -1):
				for i in range(2):
					if (score[i] >= rounds):
						run = False
						return i

			screen.blit(victory_img, (360, 150))

			if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
				round_over = False
				intro_count = 3
				fighter_1 = Fighter(1, 200, 310, False, SHAGGY_SIZE, SHAGGY_SCALE, SHAGGY_OFFSET,
						SHAGGY_sheet, SHAGGY_ANIMATION_STEPS, [punch_fx, punch_fx])
				fighter_2 = Fighter(2, 700, 310, True, HORSEMAN_SIZE, HORSEMAN_SCALE, HORSEMAN_OFFSET,
						HORSEMAN_sheet, HORSEMAN_ANIMATION_STEPS, [sword_fx, magic_fx])

		# event handler
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		pygame.display.update()

	pygame.quit()
	exit()
