#!/usr/bin/python
# -*- coding: utf-8 -*-

class Entity:
    def __init__(self, health, x, y, speed):
        self.health = health
        self.x = x
        self.y = y
        self.speed = speed
        self.is_alive = True

    def take_damage(self, amount):
        if not self.is_alive:
            return

        self.health -= amount

        if self.health <= 0:
            self.health = 0
            self.is_alive = False
