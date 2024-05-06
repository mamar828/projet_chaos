from numpy import array as nparray, sum as npsum
from pygame import joystick

from src.engines.inputs.keyboard import Keyboard
from src.engines.inputs.controller import Controller


class MasterInput:
    """
    This class defines the base class for combining inputs.
    """

    def __init__(self):
        self.inputs = [Keyboard(self)]
        joystick.init()
        for i in range(joystick.get_count()):
            self.inputs.append(Controller(self, joystick.Joystick(i)))

        if len(self.inputs) == 1:
            self.get_movement_dict = self._get_single_movement_dict
            self.get_rotation_dict = self._get_single_rotation_dict
        else:
            self.get_movement_dict = self._get_multiple_movement_dict
            self.get_rotation_dict = self._get_multiple_rotation_dict

    @staticmethod
    def multiply_dicts(dicts: list):
        # Find index of a non empty dictionary
        for i, dict_i in enumerate(dicts):
            if dict_i:
                break

        # Multiply all non empty dictionaries
        product_dict = {
            key : npsum([dict_i.get(key) for dict_i in dicts])
            for key in dicts[i].keys()
        }
        return product_dict

    def _get_single_movement_dict(self):
        return self.inputs[0].get_movement_dict()

    def _get_multiple_movement_dict(self):
        return self.multiply_dicts([input_i.get_movement_dict() for input_i in self.inputs])

    def _get_single_rotation_dict(self):
        return self.inputs[0].get_rotation_dict()

    def _get_multiple_rotation_dict(self):
        return self.multiply_dicts([input_i.get_rotation_dict() for input_i in self.inputs])
