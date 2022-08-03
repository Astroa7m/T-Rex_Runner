import pygame


class Score:

    def __init__(self, t_game):
        self.font = pygame.font.Font("assets/font/PressStart2P-Regular.ttf", 25)
        self.high_score = 1000
        self.current_score = 0000
        self.score_text = f"HI {self.high_score} 00000"
        self.text_color = (83, 83, 83)
        self.image = self.font.render(self.score_text, True, self.text_color)
        self.rect = self.image.get_rect()
        self.screen = t_game.screen
        self.screen_rect = self.screen.get_rect()
        self._set_location()

    def update_score(self, deci):
        score = self.get_formatted_score(deci)
        self.score_text = f"HI {self.high_score} {score}"
        self.image = self.font.render(self.score_text, True, self.text_color)
        self._set_location()
        self.screen.blit(self.image, self.rect)

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
        else:
            return deci

    def _set_location(self):
        self.rect.right = self.screen_rect.right - 16
        self.rect.top = self.screen_rect.top + 16


class Text:
    def __init__(self, t_game, text):
        self.font = pygame.font.Font("assets/font/PressStart2P-Regular.ttf", 30)
        self.text_color = (83, 83, 83)
        self.image = self.font.render(text.upper(), True, self.text_color)
        self.rect = self.image.get_rect()
        self.screen = t_game.screen
        self.screen_rect = self.screen.get_rect()
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
