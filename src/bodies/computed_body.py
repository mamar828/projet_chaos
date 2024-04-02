from numpy.random import randint
from random import choice
from eztcolors import Colors as C

from src.bodies.gravitational_body import GravitationalBody



class ComputedBody(GravitationalBody):
    def __init__(self, positions: list, type: str, iterations_survived: int=None, *args, **kwargs):
        """
        Defines required parameters.

        Parameters
        ----------
        positions : list
            Specifies the positions of the body at every time step.
        type : str
            Specifies the body's type. Supported types are: "base_body", "alive" and "dead".
        iterations_survived : int
            Number of iterations the body has survived in its simulation.
        args : list
            Arguments to pass to the GravitationalBody constructor.
        kwargs : dict
            Arguments to pass to the GravitationalBody constructor.
        """
        super().__init__(*args, **kwargs)
        self.positions = positions
        self.type = type
        self.iterations_survived = iterations_survived

    def __str__(self):
        return super().__str__() + f"type: {self.type}, len(positions): {len(self.positions)}"

    def update(self):
        """
        Update the body's position.
        """
        if self.positions:
            self._position = self.positions[0]
            del self.positions[0]
        else:
            self.dead = True

    def get_color(self, random_tuple=True) -> str | tuple[int, int, int]:
        """
        Get the color of the body depending on its type.

        Parameters
        ----------
        random_tuple : bool, optional
            Wether the function is allowed to return a tuple of ints or should always return a named color.

        Returns
        -------
        color : str | tuple[int, int, int]
            The color of the body: green if it stays alive, red if not and random for the others.
        """
        if self.type == "base_body" or self.type == "attractive_moving":
            if random_tuple:
                return randint(0, 255, 3)
            else:
                # red, green and black are not present
                return choice(["blue", "yellow", "orange", "cyan", "magenta", "white", "purple", "brown", "grey"])
        elif self.type == "alive":
            return "green"
        elif self.type == "dead":
            return "red"
        else:
            raise ValueError(f"self.type: {C.RED+C.BOLD}{self.type} is not a supported type.{C.END}")
