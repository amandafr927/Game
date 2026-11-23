
import pygame
from Code.Entity import Entity


class Enemy(Entity):

    def __init__(self, enemy_type, x, y):
        if enemy_type == 'ghoul':
            super().__init__(
                health=50,
                x=x,
                y=y,
                speed=2
            )

            self.frame_width = 57
            self.frame_height = 60
            self.image_size = (114, 120)
            self.filename = './asset/burning-ghoul.png'
            self.frame_count = 8
            self.damage = 5

        elif enemy_type == 'hound':
            super().__init__(
                health=40,
                x=x,
                y=y,
                speed=3
            )

            self.frame_width = 67
            self.frame_height = 32
            self.image_size = (134, 64)
            self.filename = './asset/hell-hound-run.png'
            self.frame_count = 5
            self.damage = 5

        else:
            raise ValueError("Inimigo desconhecido")
        self.damage_cooldown = 1000
        self.last_damage = 0
        self.enemy_type = enemy_type

        self.animations = {
            'idle': []
        }

        self.current_animation = 'idle'
        self.frame_index = 0
        self.last_update = pygame.time.get_ticks()

        self.load_sprites()
        self.image = self.animations['idle'][0]

    def load_animation(self):
        sheet = pygame.image.load(self.filename).convert_alpha()

        animation = []

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

            animation.append(frame)

        return animation

    def load_sprites(self):
        self.animations['idle'] = self.load_animation()

    def animate(self):
        now = pygame.time.get_ticks()

        if now - self.last_update >= 120:
            self.last_update = now

            self.frame_index += 1

            if self.frame_index >= len(self.animations[self.current_animation]):
                self.frame_index = 0

        self.image = self.animations[self.current_animation][self.frame_index]

    def update(self, player):
        if not self.is_alive or not player.is_alive:
            return

        distance = abs(self.x - player.x)

        if distance > 350:
            return

        enemy_rect = self.image.get_bounding_rect().move(
            self.x, self.y
        )

        player_rect = player.image.get_bounding_rect().move(
            player.x + player.image_offset_x, player.y
        )

        if enemy_rect.colliderect(player_rect):

            now = pygame.time.get_ticks()

            if not player.is_defending:
                if now - self.last_damage >= self.damage_cooldown:
                    player.take_damage(self.damage)
                    self.last_damage = now

            return

        enemy_center = enemy_rect.centerx
        player_center = player_rect.centerx

        if player_center > enemy_center:
            self.x += self.speed

        elif player_center < enemy_center:
            self.x -= self.speed
