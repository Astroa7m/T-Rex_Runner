import random

import pygame


class TRex(pygame.sprite.Sprite):
    def __init__(self, t_game, y):
        super().__init__()
        # init walking images
        self.trex_walking_sprites = []
        self._init_walk()
        # init crouching images
        self.trex_crouching_sprites = []
        self._init_crouching()
        # init jumping image
        self.jump_image = pygame.image.load("assets/t-rex/t-rex-0.png").convert_alpha()

        # setting current image to start animating with walking images
        self.current_sprite_index = 0
        self.image = self.trex_walking_sprites[self.current_sprite_index]
        self.rect = self.image.get_rect()
        self.rect.center = (self.rect.width, self.rect.height)
        self.y = y
        self.rect.y = self.y - self.rect.height * 0.5
        self.settings = t_game.settings
        self.screen = t_game.screen
        self.screen_rect = self.screen.get_rect()

        # trex attributes
        self.jump_count = self.settings.jump_count
        self.jumping = False
        self.crouching = False
        self.jump = False

    def update(self):
        self._set_y()
        if not self.jumping and not self.crouching:
            self._animate_through(sprites_list=self.trex_walking_sprites)
        elif self.jumping:
            self._jump()
        elif self.crouching:
            self.jump_count = self.settings.jump_count
            self._animate_through(sprites_list=self.trex_crouching_sprites)

    def _set_y(self):
        if not self.crouching and not self.jumping:
            self.rect.y = self.y - self.rect.height * 0.5
        elif self.crouching:
            self.rect.y = self.y - self.rect.height * 0.12

    def _animate_through(self, sprites_list):
        self.current_sprite_index += self.settings.character_animation_velocity
        if self.current_sprite_index >= len(sprites_list):
            self.current_sprite_index = 0
        self.image = sprites_list[int(self.current_sprite_index)]

    def _init_walk(self):
        self.trex_walking_sprites.append(pygame.image.load("assets/t-rex/t-rex-1.png").convert_alpha())
        self.trex_walking_sprites.append(pygame.image.load("assets/t-rex/t-rex-2.png").convert_alpha())

    def _init_crouching(self):
        self.trex_crouching_sprites.append(pygame.image.load("assets/t-rex/t-rex-5.png").convert_alpha())
        self.trex_crouching_sprites.append(pygame.image.load("assets/t-rex/t-rex-6.png").convert_alpha())

    def _jump(self):
        self.image = self.jump_image
        if self.jump_count >= -self.settings.jump_count:
            # identify whether the sprite is moving against the gravity
            status = 1
            if self.jump_count < 0:
                status = -1
            self.rect.y -= ((self.jump_count ** 2) * 0.5 * status) / 2
            self.jump_count -= 1
        else:
            self.jumping = False
            self.jump_count = self.settings.jump_count


class Ground(pygame.sprite.Sprite):
    def __init__(self, t_game):
        super().__init__()
        self.image = pygame.image.load("assets/ground/ground.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.settings = t_game.settings
        self.screen = t_game.screen
        self.screen_rect = self.screen.get_rect()
        self.rect.y = self.screen_rect.height * 0.75

    def should_attach_another_ground(self):
        return self.rect.right <= self.screen_rect.right

    def set_left(self, right):
        self.rect.left = right - 5

    def _check_kill(self):
        if self.rect.right <= self.screen_rect.left:
            self.kill()

    def update(self):
        self._check_kill()
        self.rect.x -= self.settings.ground_velocity


class Cloud(pygame.sprite.Sprite):
    def __init__(self, t_game, extra_x=0):
        super().__init__()
        self.image = pygame.image.load("assets/cloud/cloud.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.settings = t_game.settings
        self.screen = t_game.screen
        self.screen_rect = self.screen.get_rect()
        x = self.screen_rect.width + self.rect.width + extra_x
        y = random.randrange(self.screen_rect.height * .40, self.screen_rect.height * .65)
        self.rect.center = (x, y)

    def _check_kill(self):
        if self.rect.right < 0:
            self.kill()

    def update(self):
        self.rect.x -= self.settings.cloud_velocity
        self._check_kill()


class Cactus(pygame.sprite.Sprite):
    def __init__(self, t_game, extra_y, current_x):
        super().__init__()
        super().__init__()
        self.id = random.randrange(13)
        cactus_file = f"assets/cactus/cactus-{self.id}.png"
        self.image = pygame.image.load(cactus_file).convert_alpha()
        self.rect = self.image.get_rect()
        self.screen = t_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = t_game.settings
        if current_x:
            x = current_x + self.rect.width / 2
        else:
            x = self.screen_rect.width
        y = extra_y - self.rect.height / 3
        self.rect.center = (x, y)

    def update(self):
        self.rect.x -= self.settings.ground_velocity
        self._check_kill()

    def _check_kill(self):
        if self.rect.right < 0:
            self.kill()


class Star(pygame.sprite.Sprite):
    def __init__(self, t_game, extra_x):
        super().__init__()
        star_file = f"assets/star/star-{random.randrange(1, 4)}.png"
        self.image = pygame.image.load(star_file).convert_alpha()
        self.rect = self.image.get_rect()
        self.settings = t_game.settings
        self.screen = t_game.screen
        self.screen_rect = self.screen.get_rect()
        self.x = float(self.screen_rect.width + self.rect.width + extra_x)
        self.y = float(random.randrange(self.screen_rect.height * .45, self.screen_rect.height * .60))
        self.rect.center = (self.x, self.y)

    def update(self):
        self.x -= float(self.settings.star_velocity)
        self.rect.center = (self.x, self.y)
        self._check_kill()

    def _check_kill(self):
        if self.rect.right < 0:
            self.kill()


class Bird(pygame.sprite.Sprite):
    def __init__(self, t_game, list_of_ys):
        super().__init__()
        self.bird_sprites = []
        self.bird_sprites.append(pygame.image.load("assets/bird/bird-1.png"))
        self.bird_sprites.append(pygame.image.load("assets/bird/bird-2.png"))
        self.current_sprite_index = 0
        self.image = self.bird_sprites[self.current_sprite_index]
        self.rect = self.image.get_rect()
        self.screen_rect = t_game.screen_rect
        self.settings = t_game.settings
        # todo fix this later
        # generating random number between the list of y length
        # as 0 is top, 1 is center, 2 is bottom of the trex
        # in order to place the y of the bird correctly
        index = random.randint(0, len(list_of_ys))
        self.y = 0
        print(index)
        if index == 0:
            self.rect.top = list_of_ys[0]
        elif index == 1:
            self.rect.bottom = list_of_ys[0]
        elif index == 2:
            self.rect.bottom = list_of_ys[1]

        self.rect.x = self.screen_rect.width

    def update(self):
        self._animate_through()
        self.rect.x -= self.settings.bird_velocity
        self._check_kill()

    def _check_kill(self):
        if self.rect.right < 0:
            self.kill()

    def _animate_through(self):
        self.current_sprite_index += self.settings.bird_animation_velocity
        if self.current_sprite_index >= len(self.bird_sprites):
            self.current_sprite_index = 0
        self.image = self.bird_sprites[int(self.current_sprite_index)]
