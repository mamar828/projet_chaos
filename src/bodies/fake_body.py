from numpy import arctan2, cos, pi, sin

from src.bodies.gravitational_body import GravitationalBody
from src.tools.vector import Vector


class FakeBody:
    """
    A class to create bodies that are updated using parametric trajectories and not the system's physics.
    """

    def __init__(self):
        """
        Defines the required parameters
        """

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
        self.type = self.__class__.__name__

    def __call__(self, attractive_bodies: list[GravitationalBody]):
        """
        Placeholder method
        """

        raise NotImplementedError

    @property
    def position(self) -> Vector:
        """
        Gives the body's position as a Vector object.

        Returns
        -------
        position : Vector
            The body's position.
        """

        return self._position

    @staticmethod
    def get_current_system_info(
            attractive_bodies: list[GravitationalBody]
    ) -> tuple[GravitationalBody, GravitationalBody, float, float, float, float, float]:
        """
        Obtains the current information about the Sun-Earth-body system positions and masses.

        Parameters
        ----------
        attractive_bodies : list[GravitationalBody]
            List of the Earth and Sun bodies.

        Returns
        -------
        Tuple : Earth Body, Sun Body, Sun mass, Earth mass, Earth-Sun distance in x, y and as a radius
        """

        earth, sun = sorted(attractive_bodies, key=lambda body: body.mass)
        M_1 = sun.mass
        M_2 = earth.mass
        delta_x = earth.position.x - sun.position.x
        delta_y = earth.position.y - sun.position.y
        R = (delta_x**2 + delta_y**2)**0.5
        return earth, sun, M_1, M_2, delta_x, delta_y, R

    def save_position(self):
        """
        Saves the current position of the body to the positions list.
        """

        self.positions.append(self._position)


class L1Body(FakeBody):
    """
    A class describing the evolution of the L1 Lagrange Point.
    """

    def __call__(self, attractive_bodies: list[GravitationalBody]):
        earth, sun, M_1, M_2, delta_x, delta_y, R = self.get_current_system_info(attractive_bodies)
        r = R * (1 - (M_2 / (3*M_1))**(1/3))

        new_x = delta_x / R * r + sun.position.x
        new_y = delta_y / R * r + sun.position.y

        self._position = Vector(new_x, new_y, 0)


class L2Body(FakeBody):
    """
    A class describing the evolution of the L2 Lagrange Point.
    """

    def __call__(self, attractive_bodies: list[GravitationalBody]):
        earth, sun, M_1, M_2, delta_x, delta_y, R = self.get_current_system_info(attractive_bodies)
        r = R * (1 + (M_2 / (3*M_1))**(1/3))

        new_x = delta_x / R * r + sun.position.x
        new_y = delta_y / R * r + sun.position.y

        self._position = Vector(new_x, new_y, 0)


class L3Body(FakeBody):
    """
    A class describing the evolution of the L3 Lagrange Point.
    """

    def __call__(self, attractive_bodies: list[GravitationalBody]):
        earth, sun, M_1, M_2, delta_x, delta_y, R = self.get_current_system_info(attractive_bodies)
        r = -  R * (1 + 17/12*(M_2/M_1))

        new_x = delta_x / R * r + sun.position.x
        new_y = delta_y / R * r + sun.position.y

        self._position = Vector(new_x, new_y, 0)


class L4Body(FakeBody):
    """
    A class describing the evolution of the L4 Lagrange Point.
    """

    def __call__(self, attractive_bodies: list[GravitationalBody]):
        earth, sun, M_1, M_2, delta_x, delta_y, R = self.get_current_system_info(attractive_bodies)

        theta = pi/3 - arctan2(- delta_y, delta_x)
        new_x = R * cos(theta) + sun.position.x
        new_y = R * sin(theta) + sun.position.y

        self._position = Vector(new_x, new_y, 0)


class L5Body(FakeBody):
    """
    A class describing the evolution of the L5 Lagrange Point.
    """

    def __call__(self, attractive_bodies: list[GravitationalBody]):
        earth, sun, M_1, M_2, delta_x, delta_y, R = self.get_current_system_info(attractive_bodies)

        theta = - pi/3 + arctan2(delta_y, delta_x)
        new_x = R * cos(theta) + sun.position.x
        new_y = R * sin(theta) + sun.position.y

        self._position = Vector(new_x, new_y, 0)
