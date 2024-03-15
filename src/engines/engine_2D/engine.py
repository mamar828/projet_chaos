import pygame as pg
import numpy as np
import sys

from src.engines.engine_2D.scene import *
from src.engines.engine_2D.models import *
from src.systems.base_system import BaseSystem


class Engine_2D:
    def __init__(self,
            window_size: tuple[int]=(1440,900),
            framerate: int=60,
            fullscreen: bool=False,
            screen_color: tuple=(0,0,0),
            system: BaseSystem=None
        ):
        self.window_size = window_size
        self.framerate = framerate
        self.screen_color = screen_color
        pg.init()

        self.screen = pg.display.set_mode(self.window_size, pg.DOUBLEBUF, 16)
        if fullscreen: pg.display.toggle_fullscreen()

        self.clock = pg.time.Clock()
        self.time = 0
        self.delta_time = 0     # Enables constant camera movement regardless of the framerate

        self.scene = Scene(self, system)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

    def render(self):
        self.screen.fill(self.screen_color)
        self.scene.update()
        pg.display.update()

    def get_time(self):
        self.time = pg.time.get_ticks() * 0.001

    def run(self):
        while True:
            self.get_time()
            self.check_events()
            self.render()
            self.delta_time = self.clock.tick(self.framerate)


# listi = [
#     {"object_instance": Flat_earth(position=(51,51)), "model": Rectangle, "color": "blue", "scale": (100,100)},
#     {"object_instance": Flat_earth(position=(849,51)), "model": Circle, "color": "yellow", "scale": (100,100)},
#     {"object_instance": t(position=(700,600)), "model": Circle, "color": "orange", "scale": (80,150)}
# ]
# app = Engine_2D(
#     window_size=(1440,900),
#     framerate=60,
#     fullscreen=True,
#     screen_color=(0,60,60),
#     system=listi
# )
# app.run()
