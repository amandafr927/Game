#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
from Code.Entity import Entity


class Player(Entity):

    def __init__(self):
        super().__init__(
        health=100,
        x=30,
        y=230,
        speed=4)

        self.Attack = None
        self.is_attacking = False
        self.Defense = None
        self.facing_right = True
        self.attack_damage = None
        self.is_defending = False


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

    def load_animation(self, filename, frames):
        sheet = pygame.image.load(filename).convert_alpha()

        animation = []

        for i in range(frames):
            frame = sheet.subsurface(
                (i * 128, 0, 128, 128)
            )
            frame = pygame.transform.scale(frame, (192, 192))
            animation.append(frame)

        return animation
    def load_sprites(self):

            self.animations['run'] = self.load_animation(
                './asset/Run.png', 7
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

            if now - self.last_update >= 100:
                self.last_update = now

                animation = self.animations[self.current_animation]

                if self.frame_index < len(animation) - 1:
                    self.frame_index += 1
                else:
                    if self.current_animation in ['attack1', 'attack2']:
                        self.is_attacking = False
                        self.current_animation = 'idle'

                    self.frame_index = 0

                self.image = self.animations[self.current_animation][self.frame_index]

    def move(self):
        if self.is_attacking:
            return
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.x += self.speed
            self.current_animation = 'run'
        else:
            self.current_animation = 'idle'

    def attack(self, attack_type):
        if not self.is_attacking:
            self.is_attacking = True
            self.current_animation = attack_type
            self.frame_index = 0
            self.last_update = pygame.time.get_ticks()


    def defend(self):
        pass

    def die(self):
        pass