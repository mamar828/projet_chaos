import pygame as pg
from numpy import array as nparray, where
from numpy.core import records


class Keyboard:
    def __init__(self, app):
        self.app = app

    def get_movement_array(self):
        keys_pressed = pg.key.get_pressed()
        if True in list(keys_pressed):
            # movements = nparray(["forward", "backward", "left", "right", "up", "down"])
            keys_array = nparray([
                int(keys_pressed[pg.K_a]) - int(keys_pressed[pg.K_d]),
                int(keys_pressed[pg.K_SPACE]) - int(keys_pressed[pg.K_LSHIFT]),
                int(keys_pressed[pg.K_w]) - int(keys_pressed[pg.K_s])
            ])
            # key_values = where(key_bools, 1, 0)
            # return records.fromarrays((movements, key_values), names="movements,keys_value")
            return keys_array
        else:
            return None

    def get_rotation_array(self):
        raise NotImplemented