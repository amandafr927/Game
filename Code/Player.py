#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
from Code.Entity import Entity


class Player(Entity):

    def __init__(self):
        super().__init__(
        health=200,
        x=30,
        y=230,
        speed=6)

        self.image_offset_x = None
        self.Attack = None
        self.is_attacking = False
        self.Defense = None
        self.facing_right = True
        self.attack_damage = None
        self.hit_enemies = set()
        self.is_defending = False
        self.death_animation_finished = False

        self.animations = {
            'run': [],
            'attack1': [],
            'attack2': [],
            'defend': [],
            'death': [],
            'idle': []
        }


        self.current_animation = 'idle'
        self.frame_index = 0
        self.last_update = pygame.time.get_ticks()
        self.load_sprites()
        self.image = self.animations['idle'][0]

    def load_animation(self, filename, frames, align=False):

        sheet = pygame.image.load(filename).convert_alpha()

        animation = []

        for i in range(frames):
            frame = sheet.subsurface(
                (i * 128, 0, 128, 128)
            ).copy()

            if align:
                bounds = frame.get_bounding_rect(min_alpha=1)

                sprite = frame.subsurface(bounds).copy()

                canvas = pygame.Surface((128, 128), pygame.SRCALPHA)

                x = (128 - sprite.get_width()) // 2
                y = 128 - sprite.get_height()

                canvas.blit(sprite, (x, y))

                frame = canvas

            frame = pygame.transform.scale(frame, (192, 192))

            animation.append(frame)

        return animation

    def load_sprites(self):

            self.animations['run'] = self.load_animation(
            './asset/Run.png', 6, align=True
            )

            self.animations['attack1'] = self.load_animation(
                './asset/Attack 1.png', 5
            )

            self.animations['attack2'] = self.load_animation(
                './asset/Attack 2.png', 4
            )

            self.animations['defend'] = self.load_animation(
                './asset/Defend.png', 5
            )

            self.animations['death'] = self.load_animation(
                './asset/Dead.png', 6
            )

            self.animations['idle'] = self.load_animation(
                './asset/Idle.png', 4
            )

    def animate(self):

            now = pygame.time.get_ticks()

            animation = self.animations[self.current_animation]

            if now - self.last_update >= 80:
                self.last_update = now

                if self.current_animation == 'death':

                    if self.frame_index < len(animation) - 1:
                        self.frame_index += 1
                    else:
                        self.death_animation_finished = True

                else:
                    self.frame_index += 1

                    if self.frame_index >= len(animation):

                        if self.current_animation in ['attack1', 'attack2']:
                            self.is_attacking = False
                            self.current_animation = 'idle'

                        self.frame_index = 0

            frame = self.animations[self.current_animation][self.frame_index]

            if not self.facing_right:
                self.image = pygame.transform.flip(frame, True, False)
                self.image_offset_x = 0
            else:
                self.image = frame
                self.image_offset_x = 0

    def change_animation(self, animation):
        if self.current_animation != animation:
            self.current_animation = animation
            self.frame_index = 0
            self.last_update = pygame.time.get_ticks()

    def move(self):
        if not self.is_alive:
            return
        if self.is_attacking or self.is_defending:
            return

        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.facing_right = True
            self.change_animation('run')
            self.x += self.speed

        elif keys[pygame.K_a]:
            self.facing_right = False
            self.change_animation('run')
            self.x -= self.speed

        else:
            self.change_animation('idle')


    def attack(self, attack_type):
        if not self.is_alive:
            return
        if not self.is_attacking and not self.is_defending:
            self.is_attacking = True
            self.current_animation = attack_type
            self.frame_index = 0
            self.last_update = pygame.time.get_ticks()
            if attack_type == 'attack1':
                self.attack_damage = 20
            elif attack_type == 'attack2':
                self.attack_damage = 20
            self.hit_enemies.clear()

    def get_attack_rect(self):
        player_rect = self.image.get_bounding_rect().move(
            self.x + self.image_offset_x,
            self.y
        )

        if self.facing_right:
            return pygame.Rect(
                player_rect.right,
                player_rect.top + 25,
                110,
                player_rect.height - 50
            )
        else:
            return pygame.Rect(
                player_rect.left - 110,
                player_rect.top + 25,
                110,
                player_rect.height - 50
            )

    def defend(self, defending):
        if not self.is_alive:
            return
        if self.is_attacking:
            return

        if defending:
            if not self.is_defending:
                self.is_defending = True
                self.current_animation = 'defend'
                self.frame_index = 0
                self.last_update = pygame.time.get_ticks()

        else:
            if self.is_defending:
                self.is_defending = False
                self.current_animation = 'idle'
                self.frame_index = 0
                self.last_update = pygame.time.get_ticks()

    def take_damage(self, amount):
        if not self.is_alive:
            return

        super().take_damage(amount)

        if not self.is_alive:
            self.die()


    def die(self):
        if self.current_animation == 'death':
            return

        self.is_attacking = False
        self.is_defending = False

        self.current_animation = 'death'
        self.frame_index = 0
        self.last_update = pygame.time.get_ticks()

