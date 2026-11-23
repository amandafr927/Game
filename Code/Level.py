#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame

from Code.Entity import Entity
from Code.Player import Player
from Code.Enemy import Enemy
from Code.Camera import Camera
from Code.Guardian import Guardian

class Level:
    def __init__(self, window):
        self.window = window
        self.background = pygame.image.load(
            './asset/comchao.png'
        ).convert()
        self.camera = Camera ()
        scale = self.window.get_height() / self.background.get_height()
        self.player = Player()
        self.enemies = [
            Enemy('ghoul', 600, 302),
            Enemy('hound', 800, 358),
            Enemy('ghoul', 1000, 302)
        ]
        self.guardian = Guardian(
            x=1400,
            y=157
        )
        self.dialogue_active = False
        self.dialogue_lines = [
            "Did they send a mortal this time?",
            "Poor man...",
            "I am merely the guardian of this castle.",
            "I shall not stop you from entering..."

        ]

        self.dialogue_index = 0
        self.fade_out = False
        self.fade_start = None
        self.fade_duration = 1500
        new_width = int(self.background.get_width() * scale)
        new_height = self.window.get_height()

        self.background = pygame.transform.scale(
            self.background,
            (new_width, new_height)
        )
        self.rect = self.background.get_rect(topleft=(0, 0))

        self.game_over = False

    def run(self, ):
        running = True
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if self.game_over:
                        if event.key == pygame.K_RETURN:
                            self.fade_out = True
                            self.fade_start = pygame.time.get_ticks()

                        continue
                    if self.dialogue_active:
                        if event.key == pygame.K_RETURN:

                            if self.dialogue_index < len(self.dialogue_lines) - 1:
                                self.dialogue_index += 1

                            else:
                                self.fade_out = True
                                self.fade_start = pygame.time.get_ticks()

                        continue

                    if event.key == pygame.K_h:
                        self.player.take_damage(25)

                    if event.key == pygame.K_j:
                        self.player.attack('attack1')

                    if event.key == pygame.K_k:
                        self.player.attack('attack2')

            if not self.dialogue_active and not self.fade_out and not self.game_over:
                keys = pygame.key.get_pressed()

                self.player.defend(keys[pygame.K_l])
                self.player.move()
                self.check_guardian_proximity()

                self.player.x = max(
                    0,
                    min(
                        self.player.x,
                        self.background.get_width() - self.player.image.get_width()
                    )
                )

                self.player.animate()
                self.check_player_attacks()

                self.camera.update(
                    self.player,
                    self.background.get_width(),
                    self.window.get_width()
                )

                for enemy in self.enemies:
                    enemy.animate()

                    if self.player.is_alive:
                        enemy.update(self.player)

            if not self.player.is_alive and self.player.death_animation_finished:
                self.game_over = True

            self.guardian.animate()

            self.draw()

            if self.fade_out:
                elapsed = pygame.time.get_ticks() - self.fade_start

                alpha = min(
                    255,
                    int(255 * elapsed / self.fade_duration)
                )

                fade_surface = pygame.Surface(self.window.get_size())
                fade_surface.fill((0, 0, 0))
                fade_surface.set_alpha(alpha)

                self.window.blit(fade_surface, (0, 0))

                if alpha >= 255:
                    running = False

            pygame.display.flip()
            clock.tick(60)

    def draw(self):
        self.window.blit(
            self.background,
            (-self.camera.offset_x, 0)
        )

        for enemy in self.enemies:
            if enemy.is_alive:
                self.window.blit(
                    enemy.image,
                    (self.camera.apply(enemy.x), enemy.y)
                )

        self.window.blit(
            self.player.image,
            (
                self.camera.apply(self.player.x + self.player.image_offset_x),
                self.player.y
            )
        )

        self.window.blit(
            self.guardian.image,
            (
                self.camera.apply(self.guardian.x),
                self.guardian.y
            )
        )

        self.draw_dialogue()
        self.draw_health_bar()
        self.draw_game_over()
    def check_player_attacks(self):
        if not self.player.is_attacking:
            return

        attack_rect = self.player.get_attack_rect()

        for enemy in self.enemies:
            if not enemy.is_alive:
                continue

            if enemy in self.player.hit_enemies:
                continue

            enemy_rect = enemy.image.get_bounding_rect().move(
                enemy.x,
                enemy.y
            )

            if attack_rect.colliderect(enemy_rect):
                enemy.take_damage(self.player.attack_damage)
                self.player.hit_enemies.add(enemy)

    def check_guardian_proximity(self):
        if self.dialogue_active:
            return

        player_right = self.player.x + self.player.image.get_width()

        distance = self.guardian.x - player_right

        if 0 <= distance <= 2:
            self.dialogue_active = True

    def draw_dialogue(self):
        if not self.dialogue_active:
            return

        box_width = self.window.get_width() - 100
        box_height = 60

        box_x = 50
        box_y = self.window.get_height() - box_height - 15

        name_width = 190
        name_height = 25

        name_rect = pygame.Rect(
            box_x,
            box_y - name_height,
            name_width,
            name_height
        )

        pygame.draw.rect(
            self.window,
            (15, 10, 25),
            name_rect
        )

        pygame.draw.rect(
            self.window,
            (150, 120, 170),
            name_rect,
            2
        )

        name_font = pygame.font.Font(None, 21)

        name_text = name_font.render(
            "GUARDIAN DEMON",
            True,
            (220, 200, 235)
        )

        self.window.blit(
            name_text,
            (box_x + 10, box_y - 20)
        )

        pygame.draw.rect(
            self.window,
            (15, 10, 25),
            (box_x, box_y, box_width, box_height)
        )

        pygame.draw.rect(
            self.window,
            (150, 120, 170),
            (box_x, box_y, box_width, box_height),
            3
        )

        font = pygame.font.Font(None, 25)

        text = font.render(
            self.dialogue_lines[self.dialogue_index],
            True,
            (255, 255, 255)
        )

        self.window.blit(text, (box_x + 20, box_y + 18))

        small_font = pygame.font.Font(None, 18)

        hint = small_font.render(
            "ENTER",
            True,
            (180, 180, 180)
        )

        hint_rect = hint.get_rect(
            bottomright=(box_x + box_width - 15, box_y + box_height - 8)
        )

        self.window.blit(hint, hint_rect)

    def draw_health_bar(self):
        bar_width = 200
        bar_height = 18
        x = 25
        y = 20

        health_ratio = self.player.health / 200
        current_width = int(bar_width * health_ratio)

        pygame.draw.rect(
            self.window,
            (35, 25, 35),
            (x, y, bar_width, bar_height)
        )

        pygame.draw.rect(
            self.window,
            (150, 25, 40),
            (x, y, current_width, bar_height)
        )

        pygame.draw.rect(
            self.window,
            (180, 150, 180),
            (x, y, bar_width, bar_height),
            2
        )

        font = pygame.font.Font(None, 24)

        text = font.render(
            f"HP: {self.player.health}/200",
            True,
            (255, 255, 255)
        )

        self.window.blit(text, (x, y + 23))

    def draw_game_over(self):
        if not self.game_over:
            return

        font = pygame.font.Font('./asset/fonts/PublicPixel.ttf', 35)

        text = font.render(
            "GAME OVER",
            True,
            (180, 25, 40)
        )

        text_rect = text.get_rect(
            center=(
                self.window.get_width() // 2,
                self.window.get_height() // 2
            )
        )

        self.window.blit(text, text_rect)

        small_font = pygame.font.Font(None, 25)

        hint = small_font.render(
            "Pres ENTER to return to the main menu",
            True,
            (220, 220, 220)
        )

        hint_rect = hint.get_rect(
            center=(
                self.window.get_width() // 2,
                self.window.get_height() // 2 + 55
            )
        )

        self.window.blit(hint, hint_rect)