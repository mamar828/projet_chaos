from sys import exit
import pygame as pg

from src.engines.engine_2D.scene import Scene
from src.engines.global_engine import GlobalEngine


class Engine2D(GlobalEngine):
    def __init__(
            self,
            simulation,#=Simulation                 Cannot provide type due to circular imports
            window_size: tuple[int,int]=(900,900),
            framerate: int=60,
            display_clock: bool=False,
            clock_font: tuple[tuple[str,int], str]=(("Trebuchet MS", 25), "white"),
            fullscreen: bool=False,
            screen_color: tuple[int,int,int]=(0,0,0)
        ):
        super().__init__(simulation=simulation, window_size=window_size, framerate=framerate, fullscreen=fullscreen)
        self.screen_color = screen_color
        pg.init()
        self.screen = pg.display.set_mode(self.window_size, pg.DOUBLEBUF, 16)
        if fullscreen: pg.display.toggle_fullscreen()
        self.scene = Scene(self, display_clock, clock_font)
    
    def render(self):
        self.screen.fill(self.screen_color)
        self.scene.update()
        pg.display.update()

    def run(self):
        while True:
            self.get_time()
            self.check_events()
            self.render()
            self.delta_time = (self.clock.tick(self.framerate) / 1000) * self.physics_speed
            pg.display.set_caption(f"Current physics speed : x{self.physics_speed:.2e}")
            self.simulation_time += self.delta_time


# listi = [
#     {"object_instance": Flat_earth(position=(51,51)), "model": Rectangle, "color": "blue", "scale": (100,100)},
#     {"object_instance": Flat_earth(position=(849,51)), "model": Circle, "color": "yellow", "scale": (100,100)},
#     {"object_instance": t(position=(700,600)), "model": Circle, "color": "orange", "scale": (80,150)}
# ]
# app = Engine2D(
#     window_size=(1440,900),
#     framerate=60,
#     fullscreen=True,
#     screen_color=(0,60,60),
#     system=listi
# )
# app.run()
