import pygame as pg


class Keyboard:
    def __init__(self, app):
        self.app = app

    def get_movement_dict(self):
        keys_pressed = pg.key.get_pressed()
        if True in list(keys_pressed):
            keys_dict = {
                "forward" : int(keys_pressed[pg.K_w]) - int(keys_pressed[pg.K_s]),
                "right" : int(keys_pressed[pg.K_d]) - int(keys_pressed[pg.K_a]),
                "up" : int(keys_pressed[pg.K_SPACE]) - int(keys_pressed[pg.K_LSHIFT])
            }
            return keys_dict
        else:
            return {}

    def get_rotation_dict(self):
        keys_pressed = pg.key.get_pressed()
        if True in list(keys_pressed):
            keys_dict = {
                "horizontal" : int(keys_pressed[pg.K_l]) - int(keys_pressed[pg.K_j]),
                "vertical" : int(keys_pressed[pg.K_i]) - int(keys_pressed[pg.K_k])
            }
            return keys_dict
        else:
            return {}
