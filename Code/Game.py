#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame

from Code.Menu import Menu


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(size=(600, 480))
        self.player = None
        self.level = None
        self.running = None

    def start(self, ):
        pass

    def run(self):
        while True:
            menu = Menu(self.window)
            menu.run()
            pass



    # for event in pygame.event.get():
    # if event.type == pygame.QUIT:
    # pygame.quit()
    # quit()


def handle_events(self, ):
    pass


def check_game_over(self, ):
    pass
