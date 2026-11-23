import pygame


class Guardian:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.frame_width = 160
        self.frame_height = 144
        self.frame_count = 6

        self.image_size = (320, 288)

        self.frames = self.load_animation()

        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        self.animation_speed = 180
        self.last_update = pygame.time.get_ticks()

    def load_animation(self):
        sheet = pygame.image.load(
            './asset/guardian-idle.png'
        ).convert_alpha()

        frames = []

        for i in range(self.frame_count):
            frame = sheet.subsurface(
                (
                    i * self.frame_width,
                    0,
                    self.frame_width,
                    self.frame_height
                )
            ).copy()

            frame = pygame.transform.scale(
                frame,
                self.image_size
            )

            frames.append(frame)

        return frames

    def animate(self):
        now = pygame.time.get_ticks()

        if now - self.last_update >= self.animation_speed:
            self.last_update = now

            self.frame_index += 1

            if self.frame_index >= len(self.frames):
                self.frame_index = 0

            self.image = self.frames[self.frame_index]
