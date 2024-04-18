import numpy as np
import matplotlib.pyplot as plt

from src.systems.base_system import BaseSystem


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
        for body in self.list_of_bodies:
            if body.type == "fake":
                self.tracked_bodies.append(body)

    def update(self, time_step: float):
        """
        Updates the position of the bodies within the system according to their pre-computed positions.

        Parameters
        ----------
        time_step : float
            The time step during which the acceleration and velocity are considered constant, a smaller values gives
            more accurate results.
        """
        self.current_tick += time_step
        if self.current_tick > self.tick_factor:
            self.current_tick -= self.tick_factor
            for body in self.moving_bodies:
                if not body.dead:
                    body.update()

    def to_base_system(self) -> BaseSystem:
        """
        Convert the ComputedSystem to a BaseSystem
        
        Returns
        -------
        base_system : BaseSystem
            BaseSystem with all the ComputedSystem's bodies.
        """
        return BaseSystem(
            list_of_bodies=self.list_of_bodies, 
            base_potential=self._base_potential,
            n=self.n
        )
    
    def filter_bodies(self): ...
    
    def plot_bodies(self):
        """
        Plot the positions of all the bodies in the system.
        """
        position_velocity = []
        for body in self.list_of_bodies:
            position_velocity.append(body.position.x, body.position.y, body.time_survived)
        fig, ax = plt.subplots(1, 1, figsize=(8, 3), projection="3d")
        array = np.array(position_velocity)
        ax.bar3d(position_velocity[:,0], position_velocity[:,1], np.zeros_like(array[:,2]), 1, 1, array[:,2],
                 shade=True)
        plt.show()
