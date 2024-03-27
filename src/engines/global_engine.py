import pygame as pg
from sys import exit


class GlobalEngine:
    def __init__(
            self,
            simulation,
            window_size,
            framerate,
            fullscreen,
        ):
        self.simulation = simulation
        self.window_size = window_size
        self.framerate = framerate
        self.fullscreen = fullscreen

        self.clock = pg.time.Clock()
        self.time = 0
        self.delta_time = 0
        self.physics_speed = 1
        self.key_mode = "presets"
        self.key_string = ""
        self.pressed_keys = set()       # Keep track of pressed keys
        self.simulation_time = 0        # Duration time in the simulation's point of reference

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.scene.destroy()
                pg.quit()
                exit()
            else:
                self.update_physics_speed(event)

    def update_physics_speed(self, event):
        if event.type == pg.KEYDOWN:
            if self.key_mode == "presets":
                for i in range(0,10):
                    if event.key == getattr(pg, f"K_{i}"):
                        if self.key_mode == "presets":
                            self.physics_speed = round((10**(2.4)*i)**2 + 1)

            elif self.key_mode == "manual":
                if event.key == pg.K_RETURN:
                    k = self.key_string
                    if (((len(k.split("*")) == 1) != (len(k.split("/")) == 1)) and   # Check if only one * or /
                        ((k[0] == "*") != (k[0] == "/"))):        # Check that the first character is * or /
                        try:
                            number = int(k[1:])
                            if k[0] == "*":
                                self.physics_speed *= number
                            elif k[0] == "/":
                                self.physics_speed /= number
                        except Exception: pass
                        self.key_string = ""
                    else:
                        self.key_string = ""
                else:
                    if event.key == pg.K_x and pg.K_x not in self.pressed_keys:
                        self.key_string += "*"
                    if event.key == pg.K_SLASH and pg.K_SLASH not in self.pressed_keys:
                        self.key_string += "/"
                    for i in range(0,10):
                        if event.key == getattr(pg, f"K_{i}") and getattr(pg, f"K_{i}") not in self.pressed_keys:
                            self.key_string += str(i)

            if event.key == pg.K_p:
                self.key_mode = "presets"
                self.key_string = ""

            if event.key == pg.K_m:
                self.key_mode = "manual"
                self.key_string = ""
            
            self.pressed_keys.add(event.key)

        elif event.type == pg.KEYUP and event.key in self.pressed_keys:
            self.pressed_keys.remove(event.key)

    def get_time(self):
        self.time = pg.time.get_ticks() * 0.001
