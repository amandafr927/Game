#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame

from Code.Entity import Entity
from Code.Player import Player


class Level:
    def __init__(self, window, name):
        self.window = window
        self.name = name
        self.entity_list: list[Entity] = []
        self.background = pygame.image.load(
            './asset/comchao.png'
        ).convert()
        scale = self.window.get_height() / self.background.get_height()
        self.player = Player()

        new_width = int(self.background.get_width() * scale)
        new_height = self.window.get_height()

        self.background = pygame.transform.scale(
            self.background,
            (new_width, new_height)
        )
        self.rect = self.background.get_rect(topleft=(0, 0))
        self.enemies = None

    def run(self, ):
        running = True
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_j:
                        self.player.attack('attack1')

                    if event.key == pygame.K_k:
                        self.player.attack('attack2')
            self.player.move()
            self.player.animate()

            self.draw()

            pygame.display.flip()
            clock.tick(60)

    def draw(self, ):
        self.window.blit(self.background, self.rect)
        player_image = self.player.animations['idle'][0]

        self.window.blit(self.player.image, (self.player.x, self.player.y))

    def check_victory(self, ):
        pass
