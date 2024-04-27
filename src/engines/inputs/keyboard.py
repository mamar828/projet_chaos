import pygame as pg


class Keyboard:
    def __init__(self, master_input):
        self.master_input = master_input
        self.current_pressed_keys = set()

    def get_movement_dict(self):
        keys_pressed = pg.key.get_pressed()
        if True in list(keys_pressed):
            keys_dict = {
                "forward" : int(keys_pressed[pg.K_w]) - int(keys_pressed[pg.K_s]),
                "right" : int(keys_pressed[pg.K_d]) - int(keys_pressed[pg.K_a]),
                "up" : int(keys_pressed[pg.K_SPACE]) - int(keys_pressed[pg.K_LSHIFT])
            }
        else:
            keys_dict = {
                "forward" : 0,
                "right" : 0,
                "up" : 0
            }
        return keys_dict

    def get_rotation_dict(self):
        keys_pressed = pg.key.get_pressed()
        if True in list(keys_pressed):
            keys_dict = {
                "horizontal" : int(keys_pressed[pg.K_l]) - int(keys_pressed[pg.K_j]),
                "vertical" : int(keys_pressed[pg.K_i]) - int(keys_pressed[pg.K_k])
            }
        else:
            keys_dict = {
                "horizontal" : 0,
                "vertical" : 0
            }
        return keys_dict
