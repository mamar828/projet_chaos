import pygame as pg
from sys import exit

from src.engines.inputs.master_input import MasterInput
from src.engines.inputs.keyboard import Keyboard
from src.engines.inputs.controller import Controller
from src.engines.display import Display

class GlobalEngine:
    def __init__(
            self,
            simulation,
            window_size,
            framerate,
            fullscreen
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
        
        self.current_preset_i = 0
        self.key_string = ""
        self.pressed_inputs = set()       # Keep track of pressed keys
        self.simulation_time = 0          # Duration time in the simulation's point of reference
        
        self.input = MasterInput()
        self.display = Display(self)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.scene.destroy()
                pg.quit()
                exit()
            else:
                self.filter_event(event)

    def check_keyboard_event(self, event):
        if self.key_mode == "presets":
            for i in range(0,10):
                if event.key == getattr(pg, f"K_{i}"):
                    if self.key_mode == "presets":
                        self.physics_speed = round((10**(2.4)*i)**2 + 1)
                        self.current_preset_i = i

        elif self.key_mode == "manual":
            if event.key == pg.K_RETURN:
                k = self.key_string
                if self.is_int(k[1:]):
                    number = int(k[1:])
                    if k[0] == "*":
                        self.physics_speed *= number
                    elif k[0] == "/":
                        self.physics_speed /= number
                    elif k[0] == "+":
                        self.physics_speed += number
                    elif k[0] == "-":
                        self.physics_speed -= number
                self.key_string = ""
            else:
                if event.key == pg.K_x :
                    self.key_string += "*"
                if event.key == pg.K_SLASH:
                    self.key_string += "/"
                if event.key == pg.K_EQUALS and (pg.K_LSHIFT in self.pressed_inputs
                                                 or pg.K_RSHIFT in self.pressed_inputs):
                    self.key_string += "+"
                if event.key == pg.K_MINUS:
                    self.key_string += "-"
                for i in range(0,10):
                    if event.key == getattr(pg, f"K_{i}"):
                        self.key_string += str(i)
        
        elif self.key_mode == "camera":
            for i in range(1,10):
                if event.key == getattr(pg, f"K_{i}"):
                    if i <= 5:
                        self.camera.current_speed_modifier = 1 / 5**3 * i**3
                    else:
                        self.camera.current_speed_modifier = 1 / 5**6 * i**6
                    self.camera.current_speed_modifier_i = i
                    break

        if event.key == pg.K_TAB and "camera" in self.key_modes:
            self.camera.cycle_tracked_bodies()

        if event.key == pg.K_t and "camera" in self.key_modes:
            self.camera.cycle_movement_modes()

        if event.key == pg.K_p:
            self.key_mode = "presets"
            self.key_string = ""

        if event.key == pg.K_m:
            self.key_mode = "manual"
            self.key_string = ""

        if event.key == pg.K_c and "camera" in self.key_modes:
            self.key_mode = "camera"
            self.key_string = ""

    def check_controller_event(self, event):
        if self.key_mode == "presets":
            if event.button == 11:
                self.current_preset_i += 1
            elif event.button == 12:
                self.current_preset_i -= 1
            self.current_preset_i = max(self.current_preset_i, 0)
            self.physics_speed = round((10**(2.4)*self.current_preset_i)**2 + 1)

        elif self.key_mode == "camera":
            if event.button == 11:
                self.camera.current_speed_modifier_i += 1
            elif event.button == 12:
                self.camera.current_speed_modifier_i -= 1
            self.camera.current_speed_modifier_i = max(self.camera.current_speed_modifier_i, 0)
            if self.camera.current_speed_modifier_i <= 5:
                self.camera.current_speed_modifier = 1 / 5**3 * self.camera.current_speed_modifier_i**3
            else:
                self.camera.current_speed_modifier = 1 / 5**6 * self.camera.current_speed_modifier_i**6

        if event.button == 0 and "camera" in self.key_modes:
            self.camera.cycle_tracked_bodies()

        if event.button == 1 and "camera" in self.key_modes:
            self.camera.cycle_movement_modes()

        if event.button == 14:
            current_mode_1 = self.key_modes.index(self.key_mode)
            self.key_mode = self.key_modes[(current_mode_1 + 1) % len(self.key_modes)]
            self.key_string = ""

        if event.button == 13:
            current_mode_1 = self.key_modes.index(self.key_mode)
            self.key_mode = self.key_modes[(current_mode_1 - 1 + len(self.key_modes)) % len(self.key_modes)]
            self.key_string = ""
            
    def filter_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key not in self.pressed_inputs:
                self.check_keyboard_event(event)
                self.pressed_inputs.add(event.key)

        elif event.type == pg.KEYUP and event.key in self.pressed_inputs:
            self.pressed_inputs.remove(event.key)

        elif event.type == pg.JOYBUTTONDOWN:
            if event.button not in self.pressed_inputs:
                self.check_controller_event(event)
                self.pressed_inputs.add(event.button)
        
        elif event.type == pg.JOYBUTTONUP and event.button in self.pressed_inputs:
            self.pressed_inputs.remove(event.button)

    @staticmethod
    def is_int(value):
        try:
            int(value)
            return True
        except ValueError:
            return False

    def get_time(self):
        self.time = pg.time.get_ticks() * 0.001
