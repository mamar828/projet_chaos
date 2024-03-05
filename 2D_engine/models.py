import pygame as pg


class Base_model:
    def __init__(self, screen, position=(0,0), scale=(1,1), color="white", instance=None):
        self.instance = instance
        self.screen = screen
        self.repr = pg.Rect(*position, *scale)
        self.position = position
        self.scale = scale
        self.color = color
        self.update()

    def move(self, new_position):
        self.repr.topleft = new_position[0] - self.scale[0] // 2, new_position[1] - self.scale[1] // 2


class Rectangle(Base_model):
    def update(self):
        pg.draw.rect(surface=self.screen, color=self.color, rect=self.repr)


class Circle(Base_model):
    def update(self):
        pg.draw.ellipse(surface=self.screen, color=self.color, rect=self.repr)
