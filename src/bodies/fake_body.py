from numpy import cos, sin, arctan2, pi
from eztcolors import Colors as C

from src.bodies.gravitational_body import GravitationalBody
from src.tools.vector import Vector


class FakeBody:
    def __init__(self):
        self.mass = 0
        self.dead = False
        self.fixed = False
        self._position = Vector(0, 0, 0)
        self.initial_position = Vector(0, 0, 0)
        self.initial_velocity = None
        self.has_potential = False
        self.integrator = None
        self.time_survived = 1e20
        self.positions = []

    @property
    def position(self) -> Vector:
        return self._position

    def get_current_system_info(
            self,
            attractive_bodies: list[GravitationalBody]
    ) -> tuple[GravitationalBody, GravitationalBody, float, float, float, float, float]:
        earth, sun = sorted(attractive_bodies, key=lambda body: body.mass)
        M_1 = sun.mass
        M_2 = earth.mass
        delta_x = earth.position.x - sun.position.x
        delta_y = earth.position.y - sun.position.y
        R = ((delta_x)**2 + (delta_y)**2)**0.5
        return earth, sun, M_1, M_2, delta_x, delta_y, R

    def save_position(self):
        """
        Saves the current position of the body to the positions list.
        """
        self.positions.append(self._position)


class L1Body(FakeBody):
    def __call__(self, attractive_bodies: list[GravitationalBody]):
        earth, sun, M_1, M_2, delta_x, delta_y, R = self.get_current_system_info(attractive_bodies)
        r = R * (1 - (M_2 / (3*M_1))**(1/3))

        new_x = delta_x / R * r + sun.position.x
        new_y = delta_y / R * r + sun.position.y

        self._position = Vector(new_x, new_y, 0)


class L2Body(FakeBody):
    def __call__(self, attractive_bodies: list[GravitationalBody]):
        earth, sun, M_1, M_2, delta_x, delta_y, R = self.get_current_system_info(attractive_bodies)
        r = R * (1 + (M_2 / (3*M_1))**(1/3))

        new_x = delta_x / R * r + sun.position.x
        new_y = delta_y / R * r + sun.position.y

        self._position = Vector(new_x, new_y, 0)


class L3Body(FakeBody):
    def __call__(self, attractive_bodies: list[GravitationalBody]):
        earth, sun, M_1, M_2, delta_x, delta_y, R = self.get_current_system_info(attractive_bodies)
        r = -  R * (1 + 17/12*(M_2/M_1))

        new_x = delta_x / R * r + sun.position.x
        new_y = delta_y / R * r + sun.position.y

        self._position = Vector(new_x, new_y, 0)


class L4Body(FakeBody):
    def __call__(self, attractive_bodies: list[GravitationalBody]):
        earth, sun, M_1, M_2, delta_x, delta_y, R = self.get_current_system_info(attractive_bodies)

        theta = pi/3 - arctan2(- delta_y, delta_x)
        new_x = R * cos(theta) + sun.position.x
        new_y = R * sin(theta) + sun.position.y

        self._position = Vector(new_x, new_y, 0)


class L5Body(FakeBody):
    def __call__(self, attractive_bodies: list[GravitationalBody]):
        earth, sun, M_1, M_2, delta_x, delta_y, R = self.get_current_system_info(attractive_bodies)

        theta = - pi/3 + arctan2(delta_y, delta_x)
        new_x = R * cos(theta) + sun.position.x
        new_y = R * sin(theta) + sun.position.y

        self._position = Vector(new_x, new_y, 0)
