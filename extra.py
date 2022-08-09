import pygame


class Text:
    """Parent class for most text elements"""
    def __init__(self, t_game, text=None, text_size=None):
        self.screen = t_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = t_game.settings
        self.text_size_animation_vel = self.settings.text_animation_velocity
        self.text_size = self.settings.text_size if text_size is None else text_size
        self.font = pygame.font.Font("assets/font/PressStart2P-Regular.ttf", self.text_size)
        self.text_color = self.settings.items_color
        self.text = text
        self.image = self.font.render(self.text, True, self.text_color)
        self.rect = self.image.get_rect()

    def update(self, *args):
        pass

    def blit(self, *args):
        self.screen.blit(self.image, self.rect)


class Score(Text):
    """Represents and manages everything related to player's score"""
    def __init__(self, t_game):
        self.fetch_high_score()
        super().__init__(t_game, text=f"HI {self.high_score} 00000")
        self.current_score = 0
        self.current_mile_stone = 0
        self.should_not_play_sound = False
        self._set_location()

    def update_score(self, deci, play_milestone_sound_callback):
        # checking if we passed 100 points
        if deci >= 100 and (deci % 100 == 0 or (deci - self.current_mile_stone) >= 100):
            self.current_mile_stone = deci
            if not self.should_not_play_sound:
                # if we don't have this if condition then the following block will run multiple times
                play_milestone_sound_callback()
                self.should_not_play_sound = True
                self.settings.increase_difficulty()
        else:
            self.should_not_play_sound = False
        # changing the score color so the player notices that he/she passed new milestone
        if deci > 100 and deci in range(self.current_mile_stone, self.current_mile_stone + 10):
            self.text_color = (255, 255, 0)
        else:
            self.text_color = self.settings.items_color
        self.current_score = self.get_formatted_score(deci)
        self.score_text = f"HI {self.high_score} {self.current_score}"
        self._set_high_score()
        self.image = self.font.render(self.score_text, True, self.text_color)
        self._set_location()
        self.blit()

    def fetch_high_score(self):
        """Fetching high score from local file"""
        file = None
        try:
            file = open("highest_score.txt")
            self.high_score = self.get_formatted_score(int(file.readline()))
        except FileNotFoundError:
            self.high_score = self.get_formatted_score(0)
        finally:
            if file is not None:
                file.close()

    def _set_high_score(self):
        if int(self.current_score) > int(self.high_score):
            with open("highest_score.txt", 'w+') as f:
                f.write(str(self.current_score))

    @staticmethod
    def get_formatted_score(deci):
        score_length = len(str(deci))
        if score_length == 1:
            return f"0000{deci}"
        elif score_length == 2:
            return f"000{deci}"
        elif score_length == 3:
            return f"00{deci}"
        elif score_length == 4:
            return f"0{deci}"
        elif score_length == 0:
            return f"00000"
        else:
            return deci

    def _set_location(self):
        self.rect.right = self.screen_rect.right - 16
        self.rect.top = self.screen_rect.top + 16


class StartText(Text):
    """Start text class that tells the user to press any key to start the game"""
    def __init__(self, t_game, text, text_size=None):
        super().__init__(t_game, text.replace("", " ").upper().lstrip(), text_size)
        self.rect.center = self.screen_rect.center
        self.height = self.rect.height
        self.width = self.rect.width
        self.expanded = True

    def update(self):
        """Animating the the text by increasing and decreasing the text size"""
        if self.settings.text_size >= self.text_size > 15 and self.expanded:
            self.text_size -= int(self.text_size_animation_vel)
            self.text_size_animation_vel += 0.08
            self.font = pygame.font.Font("assets/font/PressStart2P-Regular.ttf", self.text_size)
            self.image = self.font.render(self.text.upper(), True, self.text_color)
            self.rect = self.image.get_rect()
            if self.text_size == 15:
                self.text_size_animation_vel = self.settings.text_animation_velocity
                self.expanded = not self.expanded
        else:
            self.text_size += int(self.text_size_animation_vel)
            self.text_size_animation_vel += 0.08
            self.font = pygame.font.Font("assets/font/PressStart2P-Regular.ttf", self.text_size)
            self.image = self.font.render(self.text.upper(), True, self.text_color)
            self.rect = self.image.get_rect()
            if self.text_size == self.settings.text_size:
                self.text_size_animation_vel = self.settings.text_animation_velocity
                self.expanded = True

    def blit(self, x, y):
        self.rect.center = (x, y)
        self.screen.blit(self.image, self.rect)


class Button:
    """Button class that represents the play again button"""
    def __init__(self, t_game):
        self.image = pygame.image.load("assets/button/button.png")
        self.rect = self.image.get_rect()
        self.screen = t_game.screen
        self.screen_rect = self.screen.get_rect()
        self.rect.center = self.screen_rect.center

    def blit(self, x, y):
        self.rect.center = (x, y)
        self.screen.blit(self.image, self.rect)


class BulletLoadingIndicator:
    """Loading indicator for bullets when the player's gun is empty"""
    def __init__(self, t_game):
        super().__init__()
        self.screen = t_game.screen
        self.screen_rect = t_game.screen.get_rect()
        self.settings = t_game.settings
        ground = t_game.ground_group.sprites()[0]
        self.rect_size = (self.settings.screen_dimen[0] / 4, self.settings.screen_dimen[1] / 24)
        self.rect_center = (self.screen_rect.width / 2, (ground.rect.center[1] + self.screen_rect.bottom) / 2)
        # outlined
        self.outlined_image = pygame.surface.Surface(self.rect_size)
        self.outlined_image_rect = self.outlined_image.get_rect()
        self.outlined_image_rect.center = self.rect_center

        # filled
        self.filled_image = pygame.surface.Surface(self.rect_size)
        self.filled_image_rect = self.filled_image.get_rect()
        self.filled_image_rect.center = self.rect_center

        # text
        text_size = self.settings.text_size
        text_color = self.settings.items_color
        font = pygame.font.Font("assets/font/PressStart2P-Regular.ttf", text_size)
        text = "reloading".replace("", " ").upper().lstrip()
        self.text_surface = font.render(text, True, text_color)
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.center = (
            self.rect_center[0], self.rect_center[1] + self.outlined_image_rect.height + self.text_rect.height / 2)

    def update(self, x):
        self.screen.blit(self.text_surface, self.text_rect)
        pygame.draw.rect(self.screen, self.settings.items_color, self.outlined_image_rect, 3)
        self.filled_image_rect.size = (self.outlined_image_rect.size[0] * x, self.filled_image_rect.size[1])
        pygame.draw.rect(self.screen, self.settings.items_color, self.filled_image_rect)


class BulletsCount(Text):
    """Bullets monitoring text that represents the current bullets in the player's gun"""
    def __init__(self, t_game, text_size=None):
        text = "bullets:".replace("", " ").upper().lstrip()
        super().__init__(t_game, text, text_size)
        self.rect.left = self.screen_rect.left + 16
        self.rect.top = self.screen_rect.top + 16

    def update(self, bullet_count):
        self.image = self.font.render(f"{self.text} {bullet_count}", True, self.text_color)
        self.blit()
