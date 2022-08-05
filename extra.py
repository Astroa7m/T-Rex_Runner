import pygame


class Score:

    def __init__(self, t_game):
        self.screen = t_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = t_game.settings
        self.font = pygame.font.Font("assets/font/PressStart2P-Regular.ttf", 25)
        self.fetch_high_score()
        self.current_score = 0000
        self.score_text = f"HI {self.high_score} 00000"
        self.text_color = self.settings.text_color
        self.image = self.font.render(self.score_text, True, self.text_color)
        self.rect = self.image.get_rect()

        self._set_location()

    def update_score(self, deci):
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
        if self.current_score > self.high_score:
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
    def __init__(self, t_game, text):
        self.screen = t_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = t_game.settings
        self.font = pygame.font.Font("assets/font/PressStart2P-Regular.ttf", 30)
        self.text_color = self.settings.text_color
        self.image = self.font.render(text.upper(), True, self.text_color)
        self.rect = self.image.get_rect()
        self.rect.center = self.screen_rect.center

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
