#!/usr/bin/python
# -*- coding: utf-8 -*-

from Entity import Entity


class Player(Entity):
    def __init__(self):
        self.Attack = None
        self.Defense = None
        self.facing_right = None
        self.attack_damage = None
        self.is_defending = None

    def move(self, ):
        pass

    def jump(self, ):
        pass

    def attack(self, ):
        pass

    def defend(self, ):
        pass
