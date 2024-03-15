import numpy as np


class Flat_earth:
    def __init__(self, position):
        self.x_position, self.y_position = position
        self.x_direction = 1
        self.y_direction = 1

    def update(self, delta_time):
        """Update the planet's position by its speed multiplied by time"""
        if self.x_position > 1390:
            self.x_direction *= -1
        if self.x_position < 50:
            self.x_direction *= -1
        if self.y_position < 50:
            self.y_direction *= -1
        if self.y_position > 850:
            self.y_direction *= -1
        self.x_position += 0.5 * delta_time * self.x_direction
        self.y_position += 0.5 * delta_time * self.y_direction

    def get_position(self):
        return self.x_position, self.y_position

class t(Flat_earth):
    def update(*a):...