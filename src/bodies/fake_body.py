from eztcolors import Colors as C

from src.tools.vector import Vector


class FakeBody:
    def __init__(
        self,
        type: str="L1"
    ):
        self.type = type
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

    def __call__(self, attractive_bodies: list):
        earth, sun = sorted(attractive_bodies, key=lambda body: body.mass)
        M_1 = sun.mass
        M_2 = earth.mass
        delta_x = earth.position.x - sun.position.x
        delta_y = earth.position.y - sun.position.y
        a = ((delta_x)**2 + (delta_y)**2)**0.5
        r = a * (1 - (M_2 / (3*M_1))**(1/3))

        new_x = delta_x / a * r + 450
        new_y = delta_y / a * r + 450

        self._position = Vector(new_x, new_y, 0)
        if self.positions == []:
            self.positions.append(self._position)

    def save_position(self):
        """
        Saves the current position of the body to the positions list.
        """
        self.positions.append(self._position)
        
    def get_color(self) -> tuple[int, int, int]:
        """
        Get the color of the body.

        Returns
        -------
        color : tuple[int, int, int]
            The color of the body.
        """
        return (117, 117, 117)
    
    @property
    def position(self) -> Vector:
        return self._position
