import pygame as pg
from numpy.random import randint


class BaseModel:
    def __init__(self,
            screen,
            position=(0,0),
            scale=(1,1),
            color="white",
            instance=None,
            plot_trace: bool=False,
            max_trace: int=2000
        ):
        self.instance = instance
        self.screen = screen
        # Reverse the y position because the y axis is inverted in pygame
        self.repr = pg.Rect(position[0], screen.get_height() - position[1], *scale)
        self.scale = scale
        self.color = color
        self.plot_trace = plot_trace
        self.max_trace = max_trace
        self.traces = []
        self.trace_repr = pg.Rect(0, 0, 1, 1)
        self.update()

    def move(self, new_position):
        # Reverse the y position because the y axis is inverted in pygame
        self.repr.center = new_position[0], self.screen.get_height() - new_position[1]
        if self.plot_trace:
            if len(self.traces) > self.max_trace:
                self.traces.pop(0)
            self.traces.append((new_position[0], self.screen.get_height() - new_position[1]))

    def trace(self):
        for trace in self.traces:
            self.trace_repr.center = trace[0], trace[1]
            pg.draw.ellipse(surface=self.screen, color=self.color, rect=self.trace_repr)


    @staticmethod
    def get_random_color():
        return randint(0, 255, 3)


class Rectangle(BaseModel):
    def update(self):
        pg.draw.rect(surface=self.screen, color=self.color, rect=self.repr)
        if self.plot_trace:
            self.trace()


class Circle(BaseModel):
    def update(self):
        pg.draw.ellipse(surface=self.screen, color=self.color, rect=self.repr)
        if self.plot_trace:
            self.trace()
