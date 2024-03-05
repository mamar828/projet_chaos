import numpy as np


a = np.array([1,2,3])
b = np.array([4,5,6])
c = np.array([7,8,9])


# print(np.hstack([a,b,c]))



class Planet:
    def __init__(self, position):
        self.x_position, self.y_position, self.z_position = position
        self.direction = 1

    def update(self, delta_time):
        """Update the planet's position by its speed multiplied by time"""
        if self.z_position > 50:
            self.direction *= -1
        if self.z_position < -50:
            self.direction *= -1
        self.z_position += 0.01 * delta_time * self.direction

    def get_position(self):
        return self.x_position, self.y_position, self.z_position


class Floor:
    def __init__(self, position):
        self.x_position, self.y_position, self.z_position = position

    def update(self, delta_time):
        """Update the planet's position by its speed multiplied by time"""
        pass

    def get_position(self):
        return self.x_position, self.y_position, self.z_position
