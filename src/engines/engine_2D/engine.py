import pygame as pg

from src.engines.engine_2D.scene import Scene
from src.engines.global_engine import GlobalEngine


class Engine2D(GlobalEngine):
    """
    This class defines the 2D engine.
    """

    def __init__(
            self,
            simulation=None, # Simulation instance
            window_size: tuple[int,int]=(900,900),
            framerate: int=60,
            display_clock: bool=False,
            clock_font: tuple[tuple[str,int], str]=(("Trebuchet MS", 25), "white"),
            fullscreen: bool=False,
            screen_color: tuple[int,int,int]=(0,0,0),
            objects: list=None
        ):
        """
        Initialize the Engine2D class.

        Parameters:
        -----------
        simulation : Simulation, optional
            Simulation instance. None if not provided.
        window_size : tuple[int,int], optional
            Window size in pixels. Default is (900,900).
        framerate : int, optional
            Desired framerate. Default is 60.
        display_clock : bool, optional
            Whether to display a clock on the screen. Default is False.
        clock_font : tuple[tuple[str,int], str], optional
            Font and size of the clock text, and its color. Default is (("Trebuchet MS", 25), "white").
        fullscreen : bool, optional
            Whether to start in fullscreen mode. Default is False.
        screen_color : tuple[int,int,int], optional
            RGB color of the screen background. Default is (0,0,0).
        objects : list, optional
            List of 2D objects to be rendered. Default is None.
        """

        self.key_modes = ["presets", "manual"]
        super().__init__(simulation=simulation, window_size=window_size, framerate=framerate, fullscreen=fullscreen)
        self.screen_color = screen_color
        pg.init()
        self.simulation = simulation
        self.objects = objects
        self.screen = pg.display.set_mode(self.window_size, pg.DOUBLEBUF, 16)
        if fullscreen: pg.display.toggle_fullscreen()
        self.scene = Scene(self, display_clock, clock_font)
    
    def render(self):
        self.screen.fill(self.screen_color)
        self.scene.update()
        pg.display.update()

    def get_current_state(self):
        state = {
            "lEngine type" : self.__class__.__name__,
            "Simulation time (s)" : f"{self.simulation_time:.2e}",
            "lWindow size" : self.window_size,
            "Physics speed" : f"{self.physics_speed:.2e}",
            "lFramerate" : f"{0 if self.delta_time ==0 else self.physics_speed / self.delta_time:.1f}",
            "Manual str" : self.key_string,
            "lNumber of inputs" : len(self.input.inputs),
            "empty2" : "   ",
            "lKey mode" : self.key_mode,
            "empty3" : "   "
        }
        return state

    def run(self):
        while self.running:
            self.get_time()
            self.check_events()
            if self.running:
                self.render()
                self.delta_time = (self.clock.tick(self.framerate) / 1000) * self.physics_speed
                pg.display.set_caption(f"Current physics speed : x{self.physics_speed:.2e}")
                self.simulation_time += self.delta_time
                self.display.update(self.get_current_state())
