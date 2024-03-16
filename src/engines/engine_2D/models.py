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
        self.trace = []
        self.update()

    def move(self, new_position):
        # Reverse the y position because the y axis is inverted in pygame
        self.repr.center = new_position[0], self.screen.get_height() - new_position[1]
        self.trace.append((new_position[0], self.screen.get_height() - new_position[1]))

    @staticmethod
    def get_random_color():
        return np.random.randint(0, 255, 3)


class Rectangle(Base_model):
    def update(self):
        pg.draw.rect(surface=self.screen, color=self.color, rect=self.repr)


class Circle(Base_model):
    def update(self):
        pg.draw.ellipse(surface=self.screen, color=self.color, rect=self.repr)
        other_repr = self.repr.copy()
        other_repr.width /= 7
        other_repr.height /= 7
        for trace in self.trace:
            other_repr.center = trace[0], trace[1]
            pg.draw.ellipse(surface=self.screen, color=self.color, rect=other_repr)
