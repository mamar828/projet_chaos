import pygame as pg
import numpy as np


class Base_model:
    def __init__(self, screen, position=(0,0), scale=(1,1), color="white", instance=None):
        self.instance = instance
        self.screen = screen
        # Reverse the y position because the y axis is inverted in pygame
        self.repr = pg.Rect(position[0], screen.get_height() - position[1], *scale)
        self.scale = scale
        self.color = color
        self.update()

    def move(self, new_position):
        # Reverse the y position because the y axis is inverted in pygame
        self.repr.topleft = new_position[0] - self.scale[0] // 2, self.screen.get_height() - (new_position[1] + self.scale[1] // 2)

    @staticmethod
    def get_random_color():
        return np.random.randint(0, 255, 3)


class Rectangle(Base_model):
    def update(self):
        pg.draw.rect(surface=self.screen, color=self.color, rect=self.repr)


class Circle(Base_model):
    def update(self):
        pg.draw.ellipse(surface=self.screen, color=self.color, rect=self.repr)
