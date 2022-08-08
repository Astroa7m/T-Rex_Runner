import sys

import pygame.time

from extra import *
from settings import Settings
from trex_game_sprites import *


class TRexRunner:
    """T-Rex Game class"""

    def __init__(self):
        """Initializing the T-Rex game class and most of its dependencies"""
        self.addition = 0
        self.settings = Settings()

        # pygame initialization logic
        pygame.init()
        self.screen = pygame.display.set_mode(self.settings.screen_dimen)
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("T-Rex Runner")
        game_icon = pygame.image.load("assets/t-rex/t-rex-7.png")
        pygame.display.set_icon(game_icon)
        self.start_jump_sound = pygame.mixer.Sound("assets/sounds/start_or_jump.wav")
        self.crash_sound = pygame.mixer.Sound("assets/sounds/crash.wav")
        self.milestone_sound = pygame.mixer.Sound("assets/sounds/milestone.wav")
        self.shoot_sound = pygame.mixer.Sound("assets/sounds/shoot.wav")
        self.first_shot_sound = pygame.mixer.Sound("assets/sounds/shot_hit_1.wav")
        self.second_shot_sound = pygame.mixer.Sound("assets/sounds/shot_hit_2.wav")
        self.clock = pygame.time.Clock()
        self.started = False
        self.show_press_any_key_to_start = True
        self.start_text = StartText(self, "press any key to start")
        # scoring
        self.score = Score(self)
        # bullets text indicator
        self.bullet_text = BulletsCount(self)
        # play again button
        self.button = Button(self)
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
        # bullets
        self._init_bullet()
        # bullets loading indicator
        self.bullet_loading_indicator = BulletLoadingIndicator(self)

    def start_game(self):
        while True:
            if not self.trex.collided:
                self.screen.fill(self.settings.screen_background_color)
                self._show_press_any_key_to_start_text()
                self._draw_sprites()
                self._create_indicator()
                self.bullet_text.update(self.get_bullet_count())
            else:
                self._show_game_over_text_and_play_again()
            self.trex_group.draw(self.screen)
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

    def _init_bullet(self):
        self.bullet_group = pygame.sprite.Group()

    def _draw_sprites(self):
        self.ground_group.draw(self.screen)
        self.moon_group.draw(self.screen)
        self.star_group.draw(self.screen)
        self.cloud_group.draw(self.screen)
        self.cactus_group.draw(self.screen)
        self.bird_group.draw(self.screen)
        self.bullet_group.draw(self.screen)
        if self.started:
            self._update_sprites()

    def _update_sprites(self):
        # getting current time to show/update some sprites
        current_time = pygame.time.get_ticks()
        self.current_time_int_deci = int((current_time - self.start_time) * 0.01)
        # updating score
        self.score.update_score(self.current_time_int_deci + self.addition, lambda: self.milestone_sound.play())
        # showing only birds after 450 deciseconds
        show_bird = self.current_time_int_deci > 0
        # starting show cacti after 40 deciseconds of starting the game
        forty_deci_passed = self.current_time_int_deci > 40
        show_cacti = forty_deci_passed and not self.cacti_count
        # starting creating stars after 600 deciseconds and if the list is there are no stars
        # we also randomize the creation of the stars by only start creating them if the deci time
        # is divisible by 1.5, so we create them at deci time 600, 900, etc.
        should_create_stars = (self.current_time_int_deci // 100) % 1.5 == 0 and not self.star_group.sprites()
        six_hundred_deci_passed = self.current_time_int_deci > 600
        # we are gonna show the moon after 850 deciseonds
        show_moon = self.current_time_int_deci > 850 and self.current_time_int_deci % 300 == 0
        # we are gonna use this variable to decide whether to show cactus or a bird
        # where 0 = show cactus and 1 a bird
        # it will start with zero and once we show birds we gonna generate it randomly
        if show_bird:
            sprite_type = random.randint(0, 1)
        else:
            sprite_type = 0

        # Update trex
        self.trex.update()
        self._check_collisions()

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
        if six_hundred_deci_passed and should_create_stars:
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
                top_of_bird = self.ground_group.sprites()[0].rect.y - self.trex.rect.height - \
                              self.ground_group.sprites()[0].rect.height * 0.75
                bottom_of_ground = self.ground_group.sprites()[0].rect.bottom
                top_of_trex = self.trex.rect.top
                list_of_ys = [top_of_bird, bottom_of_ground, top_of_trex]
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

        # Update bullets
        for bullet in self.bullet_group.sprites():
            bullet.update()

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
                if self.show_press_any_key_to_start:
                    self.start_time = pygame.time.get_ticks()
                if self.show_press_any_key_to_start:
                    self.start_jump_sound.play()
                    self.show_press_any_key_to_start = False
                self.started = True
                if event.key == pygame.K_UP:
                    if not self.trex.jumping:
                        self.start_jump_sound.play()
                    self.trex.jumping = True
                    self.trex.crouching = False
                elif event.key == pygame.K_DOWN:
                    self.trex.jumping = False
                    self.trex.crouching = True
                if event.key == pygame.K_SPACE:
                    self._fire_bullet()
            elif event.type == pygame.KEYUP:
                self.trex.crouching = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                retry_clicked = self.button.rect.collidepoint(mouse_pos)
                if self.trex.collided and retry_clicked:
                    self._reset()

    def _check_collisions(self):
        cactus_hit = pygame.sprite.spritecollide(
            self.trex,
            self.cactus_group,
            True,
            pygame.sprite.collide_mask)
        bird_hits = pygame.sprite.spritecollide(
            self.trex,
            self.bird_group,
            True,
            pygame.sprite.collide_mask)
        bullet_hit_bird = pygame.sprite.groupcollide(
            self.bullet_group,
            self.bird_group,
            True,
            False,
            pygame.sprite.collide_mask)

        for bullet in bullet_hit_bird:
            for bird in bullet_hit_bird[bullet]:
                if bird.current_list == bird.damaged_bird_sprites:
                    bird.kill()
                    self.addition += 8
                    self.second_shot_sound.play()
                    return
                bird.set_damaged()
                self.first_shot_sound.play()

        bullet_hit_cactus = pygame.sprite.groupcollide(
            self.bullet_group,
            self.cactus_group,
            True,
            False,
            pygame.sprite.collide_mask)
        for bullet in bullet_hit_cactus:
            for cactus in bullet_hit_cactus[bullet]:
                if cactus.image == cactus.damaged_image:
                    cactus.kill()
                    self.addition += 4
                    self.second_shot_sound.play()
                    return
                cactus.set_damaged()
                self.first_shot_sound.play()

        if bird_hits or cactus_hit:
            self.crash_sound.play()
            self.trex.collide()

    def _show_game_over_text_and_play_again(self):
        game_over = StartText(self, "game over", 30)
        x = self.screen_rect.centerx
        y1 = self.screen_rect.height / 3
        y2 = self.screen_rect.height - y1
        game_over.blit(x, y1)
        self.button.blit(x, y2)

    def _reset(self):
        self.start_jump_sound.play()
        self.start_time = pygame.time.get_ticks()
        self.addition = 0
        self.score.fetch_high_score()
        self._drop_sprites()
        self.trex.reset()
        self.settings.reset_difficulty()

    def _drop_sprites(self):
        self.cactus_group.empty()
        self.bird_group.empty()
        self.bullet_group.empty()
        self.star_group.empty()
        self.moon_group.empty()

    def _fire_bullet(self):
        if self.settings.bullet_count > len(self.bullet_group.sprites()) and not self.trex.collided:
            bullet = Bullet(self)
            self.bullet_group.add(bullet)
            self.shoot_sound.play()

    def _show_press_any_key_to_start_text(self):
        if self.show_press_any_key_to_start:
            self.start_text.blit(self.screen_rect.width / 2, self.screen_rect.height / 2)
            self.start_text.update()

    def _create_indicator(self):
        if self.get_bullet_count() == 0:
            percentage = 1 - ((self.settings.screen_dimen[0] - self.bullet_group.sprites()[-1].rect.x) /
                              self.settings.screen_dimen[0])
            self.bullet_loading_indicator.update(percentage)

    def get_bullet_count(self):
        return abs(len(self.bullet_group.sprites()) - self.settings.bullet_count)


if __name__ == '__main__':
    game = TRexRunner()
    game.start_game()
