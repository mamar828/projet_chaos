from numpy.random import randint
from eztcolors import Colors as C

from src.bodies.gravitational_body import GravitationalBody



class ComputedBody(GravitationalBody):
    def __init__(self, positions: list, type: str, *args, **kwargs):
        """
        Defines required parameters.

        Parameters
        ----------
        positions : list
            Specifies the positions of the body at every time step.
        type : str
            Specifies the body's type. Supported types are: "base_body", "alive" and "dead".
        *args : list
            Arguments to pass to the GravitationalBody constructor.
        """
        super().__init__(*args, **kwargs)
        self.positions = positions
        self.type = type

    def update(self):
        """
        Update the body's position.
        """
        if self.positions:
            self._position = self.positions[0]
            del self.positions[0]
        else:
            self.dead = True

    def get_color(self) -> str:
        """
        Get the color of the body depending on its type.

        Returns
        -------
        color : str
            The color of the body: green if it stays alive, red if not and random for the others.
        """
        if self.type == "base_body":
            return randint(0, 255, 3)
        elif self.type == "alive":
            return "green"
        elif self.type == "dead":
            return "red"
        else:
            raise ValueError(f"self.type: {C.RED+C.BOLD}{self.type} is not a supported type.{C.END}")
