#!/usr/bin/python
# -*- coding: utf-8 -*-

class Entity:
    def __init__(self, health, x, y, speed):
        self.health = health
        self.x = x
        self.y = y
        self.speed = speed
        self.is_alive = True

    def move(self, ):
        pass

    def take_damage(self, amount):
        pass
