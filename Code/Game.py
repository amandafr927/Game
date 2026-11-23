#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame

from Code.Const import MENU_OPTION
from Code.Level import Level
from Code.Menu import Menu


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(size=(823, 480))

    def run(self):
        pygame.display.set_caption('Knights Honor')
        while True:
            menu = Menu(self.window)
            menu_return = menu.run()

            if menu_return == MENU_OPTION[0]:
                level = Level(self.window)
                level.run()
            else:
                pygame.quit()
                quit()

