from numpy import argmax
from pickle import loads, dumps

from src.systems.base_system import BaseSystem
from src.fields.scalar_field import ScalarField
from src.tools.vector import Vector


class ComputedSystem(BaseSystem):
    def __init__(self, *args, tick_factor: int=1, **kwargs):
        """
        Initialize a ComputedSystem object.

        Arguments
        ---------
        args : list
            List of arguments to pass to the BaseSystem constructor.
        tick_factor : int
            Sets the factor by which the tick rate of the system is multiplied. Defaults to 1. This is used for viewing
            simulations in real-time which were done without saving every position.
        kwargs : dict
            Dictionary of arguments to pass to the BaseSystem constructor.
        """
        super().__init__(*args, **kwargs)
        self.tick_factor = tick_factor
        self.current_tick = 0
        # Find origin
        masses = [body.mass for body in self.list_of_bodies]
        self.origin = tuple(self.list_of_bodies[argmax(masses)].position)

    def update(self, *args, **kwargs):
        """
        Updates the position of the bodies within the system according to their pre-computed positions.
        """
        self.current_tick += 1
        if self.current_tick == self.tick_factor:
            self.current_tick = 0
            for body in self.moving_bodies:
                if not body.dead:
                    body.update()

    def get_potential_function(self) -> ScalarField:
        """ 
        Give the callable representing the potential function.

        Returns
        -------
        potential_function : ScalarField
            Function of three variables giving the potential value at the specified position.
        """
        potential_field = loads(dumps(self._base_potential))
        for body in self.attractive_bodies:
            potential_field += body.potential
        if len(potential_field.terms) > 2:
            potential_field -= ScalarField([(0, 0, Vector(0, 0, 0))])

        return loads(dumps(potential_field))*(10**(-self.n))**3
