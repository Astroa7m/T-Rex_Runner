import sys

import pygame.time

from extra import Score, Text, Button
from settings import Settings
from trex_game_sprites import *


class TRexRunner:
    """T-Rex Game class"""

    def __init__(self):
        """Initializing the T-Rex game class and most of its dependencies"""
        self.settings = Settings()

        # pygame initialization logic
        pygame.init()
        self.screen = pygame.display.set_mode(self.settings.screen_dimen)
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("T-Rex Runner")
        game_icon = pygame.image.load("assets/t-rex/t-rex-7.png")
        pygame.display.set_icon(game_icon)
        self.clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()
        # current stage is used to identify the current stage of the game

        # scoring
        self.score = Score(self)
        # play again button
        self.button = Button(self)
        self.collided_cactus = None
        self.collided_bird = None
        # init sprites

        # ground
        self._init_ground()
        self.attaching_ground = False

        # t-rex
        self._init_trex()
        # clouds
        self._init_clouds()
        # cacti
        self._init_cacti()
        self.cacti_count = 0
        self._cacti_created = False
        # star
        self._init_stars()
        # bird
        self._init_birds()
        # moon
        self._init_moon()

    def start_game(self):
        while True:
            if not self.trex.collided:
                self.screen.fill(self.settings.screen_background)
                self._draw_sprites()
            else:
                self._show_game_over_text_and_play_again()
            self._listen_for_events()
            pygame.display.flip()
            self.clock.tick(60)

    def _init_trex(self):
        self.trex_group = pygame.sprite.Group()
        sprites_y = self.ground_group.sprites()[0].rect.y - self.ground_group.sprites()[0].rect.height
        self.trex = TRex(self, sprites_y)
        self.trex_group.add(self.trex)

    def _init_ground(self):
        self.ground_group = pygame.sprite.Group()
        self._create_ground()

    def _init_clouds(self):
        self.cloud_group = pygame.sprite.Group()
        for i in range(1, 4):
            self._create_cloud(i * 250)

    def _init_cacti(self):
        self.cactus_group = pygame.sprite.Group()

    def _init_stars(self):
        self.star_group = pygame.sprite.Group()

    def _init_birds(self):
        self.bird_group = pygame.sprite.Group()

    def _init_moon(self):
        self.moon_group = pygame.sprite.Group()

    def _draw_sprites(self):
        self.ground_group.draw(self.screen)
        self.moon_group.draw(self.screen)
        self.star_group.draw(self.screen)
        self.cloud_group.draw(self.screen)
        self.cactus_group.draw(self.screen)
        self.bird_group.draw(self.screen)
        self.trex_group.draw(self.screen)
        if not self.trex.collided:
            self._update_sprites()
        self._check_collisions()

    def _update_sprites(self):
        # getting current time to show/update some of the sprites
        current_time = pygame.time.get_ticks()
        current_time_int_deci = int((current_time - self.start_time) * 0.01)
        ## updating score
        self.score.update_score(current_time_int_deci)
        # showing only birds after 450 deciseconds
        show_bird = current_time_int_deci > 50
        # starting show cacti after 40 deciseconds of starting the game
        forty_deci_passed = current_time_int_deci > 40
        show_cacti = forty_deci_passed and not self.cacti_count
        # starting creating stars after 600 deciseconds and if the list is there are no stars
        # we also randomize the creation of the stars by only start creating them if the deci time
        # is divisible by 1.5, so we create them at deci time 600, 900, etc.
        should_create = (current_time_int_deci // 100) % 1.5 == 0 and not self.star_group.sprites()
        six_hundred_deci_passed = current_time_int_deci > 600
        # we are gonna show the moon after 850 deciseonds
        show_moon = current_time_int_deci > 850 and current_time_int_deci % 300 == 0
        # we are gonna use this variable to decide whether to show cactus or a bird
        # where 0 = show cactus and 1 a bird
        # it will start with zero and once we show birds we gonna generate it randomly
        if show_bird:
            sprite_type = random.randint(0, 1)
        else:
            sprite_type = 0

        # Update trex
        self.trex.update()

        # Update ground
        for ground in self.ground_group.sprites():
            if ground.should_attach_another_ground() and len(self.ground_group) <= 1:
                self._create_ground(right=ground.rect.right)
            ground.update()

        # Update clouds
        for cloud in self.cloud_group.sprites():
            cloud.update()
        if len(self.cloud_group.sprites()) < 3:
            self._create_cloud()

        # Update star
        for star in self.star_group.sprites():
            star.update()
        if six_hundred_deci_passed and should_create:
            stars_count = random.randint(1, 3)
            for i in range(stars_count):
                star = Star(self, i * 250)
                self.star_group.add(star)

        if sprite_type == 0 and not self.bird_group.sprites():
            if show_cacti:
                self._create_cacti()
            if len(self.cactus_group.sprites()) < self.cacti_count:
                self._create_cacti()
        elif sprite_type == 1 and not self.cactus_group.sprites():
            if not self.bird_group.sprites():
                top_of_trex = self.trex.rect.top
                bottom_of_ground = self.ground_group.sprites()[0].rect.bottom
                list_of_ys = [top_of_trex, bottom_of_ground]
                bird = Bird(self, list_of_ys)
                self.bird_group.add(bird)

        # Update Cacti
        for cactus in self.cactus_group.sprites():
            cactus.update()
        # Update birds
        for bird in self.bird_group.sprites():
            bird.update()

        # Update moon
        for moon in self.moon_group.sprites():
            moon.update()
        if show_moon and not self.moon_group.sprites():
            moon = Moon(self)
            self.moon_group.add(moon)

    def _create_ground(self, right=None):
        ground = Ground(self)
        if right is not None:
            ground.set_left(right)
        self.ground_group.add(ground)

    def _create_cloud(self, x=0):
        cloud = Cloud(self, x)
        self.cloud_group.add(cloud)

    def _create_cacti(self):
        # tracking the id of each cactus to have a unique cacti in each group
        ids = []
        self.cacti_count = random.choices([1, 2, 3, 4], [.4, .2, .1, .1])[0]
        # calculating the previous cactus width and x to increase the x pos of the following cactus
        prev_x = 0
        prev_width = 0
        for _ in range(self.cacti_count):
            cactus_y = self.ground_group.sprites()[0].rect.y + self.ground_group.sprites()[0].rect.height / 2
            cactus_x = prev_x + prev_width
            cactus = Cactus(self, cactus_y, cactus_x)
            while cactus.id in ids:
                cactus = Cactus(self, cactus_y, cactus_x)
            ids.append(cactus.id)
            prev_x = cactus.rect.x
            prev_width = cactus.rect.width
            self.cactus_group.add(cactus)
            self._cacti_created = True

    def _listen_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    self.trex.jumping = True
                    self.trex.crouching = False
                if event.key == pygame.K_DOWN:
                    self.trex.jumping = False
                    self.trex.crouching = True
            elif event.type == pygame.KEYUP:
                self.trex.crouching = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.button.rect.collidepoint(mouse_pos):
                    self._reset()

    def _check_collisions(self):
        trex_birds_collision, trex_cacti_collision = False, False
        for cactus in self.cactus_group:
            trex_cacti_collision = pygame.sprite.collide_circle(self.trex, cactus)
            self.collided_cactus = cactus

        for bird in self.bird_group:
            trex_birds_collision = pygame.sprite.collide_circle(self.trex, bird)
            if trex_birds_collision:
                self.collided_bird = bird

        if trex_birds_collision or trex_cacti_collision:
            self.trex.collide()

    def _show_game_over_text_and_play_again(self):
        game_over = Text(self, "G a m e  O v e r")
        x = self.screen_rect.centerx
        y1 = self.screen_rect.height / 3
        y2 = self.screen_rect.height - y1
        game_over.blit(x, y1)
        self.button.blit(x, y2)

    def _reset(self):
        if self.collided_bird:
            self.collided_bird.kill()
        if self.collided_cactus:
            self.collided_cactus.kill()
        self.start_time = pygame.time.get_ticks()
        self.trex.collided = False



if __name__ == '__main__':
    game = TRexRunner()
    game.start_game()
