class Settings:
    def __init__(self):
        # static settings
        self.screen_dimen = (1000, 500)
        self.screen_background_color = (5, 11, 7)
        self.items_color = (141, 203, 159)
        self.character_animation_velocity = 0.2
        self.text_animation_velocity = 0
        self.bird_animation_velocity = 0.08
        self.bullet_width = 15
        self.bullet_height = 3
        self.bullet_speed = 7
        self.text_size = 20
        self.jump_count = 14
        self.gravity = 0.8
        self.fps = 25
        self.difficulty_scale = 0.01

        # nonstatic settings
        self.reset_difficulty()

    def increase_difficulty(self):
        self.cloud_velocity += self.cloud_velocity * self.difficulty_scale
        self.ground_velocity += self.ground_velocity * self.difficulty_scale
        self.star_velocity += self.star_velocity * self.difficulty_scale
        self.moon_velocity += self.moon_velocity * self.difficulty_scale
        self.bird_velocity += self.bird_velocity * self.difficulty_scale
        self.bullet_count += self.bullet_count * self.difficulty_scale

    def reset_difficulty(self):
        self.cloud_velocity = 1
        self.ground_velocity = 13
        self.star_velocity = 0.9
        self.moon_velocity = 0.8
        self.bird_velocity = 8
        self.bullet_count = 2

