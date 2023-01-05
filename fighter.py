import pygame

class Fighter():

    def __init__(self, player, x, y, flip, size, image_scale, offset, sprite_sheet, animation_steps, sounds):
        self.player = player
		self.rect = pygame.Rect((x, y, 80, 180))
        self.flip = flip
        self.size = size
        self.image_scale = image_scale
        self.offset = offset
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
		self.attack_sound = sounds
		self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.frame_index = 0
        self.vel_y = 0
		self.attack_type = 0
        self.attack_cooldown = 0
		self.health = 100
        self.running = False
        self.jump = False
        self.attacking = False
        self.hit = False
        self.alive = True

		# 0: idle
		# 1: run
		# 2: jump
		# 3: attack1
		# 4: attack2
		# 5: hit
		# 6: death
        self.action = 0

	# extract images from spritesheet
    def load_images(self, sprite_sheet, animation_steps):
        animation_list = []

        for y, animation in enumerate(animation_steps):
            temp_img_list = []

            for x in range(animation):
                temp_img = sprite_sheet.subsurface(
                    x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(
                    temp_img, (self.size * self.image_scale, self.size * self.image_scale)))

            animation_list.append(temp_img_list)

        return animation_list

    def move(self, screen_width, screen_height, surface, target, round_over):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0

        # get key presses count
        key = pygame.key.get_pressed()

        # perform other actions if not attacking
        if self.attacking == False and self.alive == True and round_over == False:
            # controls of player 1
            if self.player == 1:
                # move
                if key[pygame.K_a]:
                    dx = -SPEED
                    self.running = True

                if key[pygame.K_d]:
                    dx = SPEED
                    self.running = True

                # jump
                if key[pygame.K_w] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True

                # attack
                if key[pygame.K_r] or key[pygame.K_t]:
                    # determine attack type
                    if key[pygame.K_r]:
                        self.attack_type = 1

                    if key[pygame.K_t]:
                        self.attack_type = 2
                    
                    self.attack(target)

            # controls of player 2
            if self.player == 2:
                # move
                if key[pygame.K_LEFT]:
                    dx = -SPEED
                    self.running = True

                if key[pygame.K_RIGHT]:
                    dx = SPEED
                    self.running = True

                # jump
                if key[pygame.K_UP] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True

                # attack
                if key[pygame.K_o] or key[pygame.K_p]:
                    # determine attack type
                    if key[pygame.K_o]:
                        self.attack_type = 1

                    if key[pygame.K_p]:
                        self.attack_type = 2

                    self.attack(target)

        # exert gravity
        self.vel_y += GRAVITY
        dy += self.vel_y

        # make sure player stays within screen boundaries
        if self.rect.left + dx < 0:
            dx = -self.rect.left

        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right

        if self.rect.bottom + dy > screen_height - 110:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 110 - self.rect.bottom

        # make sure players face each other
        if target.rect.centerx > self.rect.centerx:
            self.flip = False

        else:
            self.flip = True

        # attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # modify player coordinates
        self.rect.x += dx
        self.rect.y += dy

    # perform animations
    def update(self):

        # check current action
        if self.health <= 0:
            self.health = 0
            self.alive = False
			# 6: death
            self.update_action(6)
        elif self.hit == True:
			# 5: hit
            self.update_action(5)
        elif self.attacking == True:
            if self.attack_type == 1:
				# 3: attack1
                self.update_action(3)
            elif self.attack_type == 2:
				# 4: attack2
                self.update_action(4)
        elif self.jump == True:
			# 2: jump
            self.update_action(2)
        elif self.running == True:
			# 1: run
            self.update_action(1)
        else:
			# 0: idle
            self.update_action(0)

        animation_cooldown = 100

        # update image
        self.image = self.animation_list[self.action][self.frame_index]

        # check time count since last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

        # check animation exectution status 
        if self.frame_index >= len(self.animation_list[self.action]):
            # finish the animation if the player is dead
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

                # check for execution of any attack
                if self.action == 3 or self.action == 4:
                    self.attacking = False
                    self.attack_cooldown = 20

                # check for taken damage
                if self.action == 5:
                    self.hit = False
					self.attack_cooldown = 20

                    # finish the attack if the player is in the middle of an attack
                    self.attacking = False

    def attack(self, target):
        if self.attack_cooldown == 0:
            # perform attack
            self.attacking = True

            if (self.attack_type == 1):
                self.attack_sound[0].play()
            else:
                self.attack_sound[1].play()

            attacking_rect = pygame.Rect(self.rect.centerx - (
                2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)

            if attacking_rect.colliderect(target.rect):
                if (self.attack_type == 1):
                    target.health -= 20
                else:
                    target.health -= 10

                target.hit = True

    def update_action(self, new_action):
        # compare the new action type to the current action type
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (
            self.offset[1] * self.image_scale)))
