import pygame as pg
from numpy import max as npmax, abs as npabs


class Controller:
    def __init__(self, master_input, joystick, threshold: float=0.35):
        self.master_input = master_input
        self.joystick = joystick
        self.joystick.init()
        self.threshold = threshold

    def get_movement_dict(self):
        axis = [self.joystick.get_axis(i) for i in range(self.joystick.get_numaxes())]
        if npmax(npabs(axis[:2])) > self.threshold or npmax(axis[4:]) > 0:
            keys_dict = {
                "forward" : -axis[1],
                "right" : axis[0],
                "up" : max(0, axis[4]) - max(0, axis[5])
            }
        else:
            keys_dict = {
                "forward" : 0,
                "right" : 0,
                "up" : 0
            }
        return keys_dict

    def get_rotation_dict(self):
        axis = [self.joystick.get_axis(i) for i in range(self.joystick.get_numaxes())]
        if npmax(npabs(axis[2:4])) > self.threshold:
            keys_dict = {
                "horizontal" : axis[2],
                "vertical" : -axis[3]
            }
        else:
            keys_dict = {
                "horizontal" : 0,
                "vertical" : 0
            }
        return keys_dict
