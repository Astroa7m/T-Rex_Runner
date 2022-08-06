import pygame


class Score:

    def __init__(self, t_game):
        self.screen = t_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = t_game.settings
        self.text_size = self.settings.text_size
        self.text_size_animation_vel = self.settings.text_animation_velocity
        self.font = pygame.font.Font("assets/font/PressStart2P-Regular.ttf", self.text_size)
        self.fetch_high_score()
        self.current_score = 0
        self.score_text = f"HI {self.high_score} 00000"
        self.text_color = self.settings.items_color
        self.image = self.font.render(self.score_text, True, self.text_color)
        self.rect = self.image.get_rect()
        self.current_mile_stone = 0
        self.should_not_play_sound = False
        self._set_location()

    def update_score(self, deci, play_milestone_sound_callback):
        if deci >= 100 and deci % 100 == 0:
            self.current_mile_stone = deci
            if not self.should_not_play_sound:
                play_milestone_sound_callback()
                self.should_not_play_sound = True
            self.settings.increase_difficulty()
        else:
            self.should_not_play_sound = False
        if deci > 100 and deci in range(self.current_mile_stone, self.current_mile_stone + 10):
            self.text_color = (255, 255, 0)
        else:
            self.text_color = self.settings.items_color
        self.current_score = self.get_formatted_score(deci)
        self.score_text = f"HI {self.high_score} {self.current_score}"
        self._set_high_score()
        self.image = self.font.render(self.score_text, True, self.text_color)
        self._set_location()
        self.screen.blit(self.image, self.rect)

    def fetch_high_score(self):
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


class Text:
    def __init__(self, t_game, text, text_size=None):
        self.screen = t_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = t_game.settings
        self.text_size = self.settings.text_size if text_size is None else text_size
        self.text_size_animation_vel = self.settings.text_animation_velocity
        self.font = pygame.font.Font("assets/font/PressStart2P-Regular.ttf", self.text_size)
        self.text_color = self.settings.items_color
        self.text = text
        self.image = self.font.render(self.text.upper(), True, self.text_color)
        self.rect = self.image.get_rect()
        self.rect.center = self.screen_rect.center
        self.height = self.rect.height
        self.width = self.rect.width
        self.expanded = True

    def update(self):
        if self.settings.text_size >= self.text_size > 10 and self.expanded:
            self.text_size -= int(self.text_size_animation_vel)
            self.text_size_animation_vel += 0.08
            self.font = pygame.font.Font("assets/font/PressStart2P-Regular.ttf", self.text_size)
            self.image = self.font.render(self.text.upper(), True, self.text_color)
            self.rect = self.image.get_rect()
            if self.text_size == 10:
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
    def __init__(self, t_game):
        self.image = pygame.image.load("assets/button/button.png")
        self.rect = self.image.get_rect()
        self.screen = t_game.screen
        self.screen_rect = self.screen.get_rect()
        self.rect.center = self.screen_rect.center

    def blit(self, x, y):
        self.rect.center = (x, y)
        self.screen.blit(self.image, self.rect)
