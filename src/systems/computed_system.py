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
