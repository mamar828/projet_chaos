import matplotlib.pyplot as plt
import numpy as np

from src.systems.base_system import BaseSystem
from src.bodies.fake_body import *


class ComputedSystem(BaseSystem):
    def __init__(self, *args, tick_factor: int=1, info: dict=None, **kwargs):
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
            if body.type.endswith("Body") or body.type.endswith("fake"):
                self.tracked_bodies.append(body)
                self.fake_bodies.append(body)
        self.info = info

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

        new_bodies = []
        for body in self.list_of_bodies:
            if body.time_survived == 1e20:
                try:
                    new_bodies.append(eval(f"{body.type}()"))
                except NameError:
                    # TEMPORARY, REMOVE LATER
                    new_bodies.append(L1Body())
            else:
                new_bodies.append(body)
        return BaseSystem(
            list_of_bodies=new_bodies, 
            base_potential=self._base_potential,
            n=self.n
        )
    
    def get_bodies_info(self) -> np.ndarray:
        iterated_bodies = list(set(self.list_of_bodies) - set(self.attractive_bodies) - set(self.fake_bodies))
        # Columns are : position.x, position.y, position.z, velocity.x, velocity.y, velocity.z, time_survived
        bodies_info = np.array([body.get_info() for body in iterated_bodies])
        return bodies_info[bodies_info[:,4].argsort()]
    
    def plot_bodies(self, bar3d: bool=False, save_filename: str=None):
        """
        Plot the positions of all the bodies in the system.
        """

        filtered_bodies = self.get_bodies_info()
        number_of_positions = int(self.info["simulation_count"])
        for i in range(int(self.info["bodies_per_simulation"])):
            current_data = filtered_bodies[i*number_of_positions:(i+1)*number_of_positions]
            fig = plt.figure()
            plt.tight_layout()

            if bar3d:
                ax1 = fig.add_subplot(projection='3d')
                ax1.set_zlabel("Temps de survie [s]")
                ax1.bar3d(current_data[:,0], current_data[:,1], np.zeros_like(current_data[:,0]), 1, 1, 
                          current_data[:,6], shade=True, color="green")
            else:
                ax1 = fig.add_subplot()
            
            ax1.set_title(f"Current velocity: {current_data[0,3]:.5e},  {current_data[0,4]:.5e}")
            ax1.set_xlabel("Distance horizontale avec le Soleil [Gm]")
            ax1.set_ylabel("Distance verticale avec le Soleil [Gm]")

            plt.gca
            plt.gcf

            ax1.scatter(np.abs(current_data[:,0]-450), np.abs(current_data[:,1]-450), c=current_data[:,6])

            if save_filename:
                fig.set_size_inches(7.5, 9)
                plt.savefig(save_filename, dpi=600)
            else:
                plt.show()
    
    def create_subplot(
            self,
            axis,
            multiplication_factors: tuple[int,int]=(1,1),
            bar3d: bool=False,
            plot_best_body: bool=True,
            **kwargs
        ):
        """
        Plot the positions of all the bodies in the system.
        """

        filtered_bodies = self.get_bodies_info()
        number_of_positions = int(self.info["simulation_count"])
        if plot_best_body:
            # Determine the velocity that will be plotted by using the velocity which has the longest surviving body
            vel = np.argmax(filtered_bodies[:,6]) // number_of_positions
        else:
            vel = 0
        
        current_data = filtered_bodies[vel*number_of_positions:(vel+1)*number_of_positions]
        if bar3d:
            y = np.abs(450 - current_data[:,1]) * multiplication_factors[1]
            x = np.abs(450 - current_data[:,0]) * multiplication_factors[0]
            z = current_data[:,6] / (8766*3600)
            axis.bar3d(x, y, np.zeros(current_data.shape[0]), np.ptp(x)/30, np.ptp(y)/30, z, shade=True, color="green")
        else:
            x = np.abs(450 - current_data[:,0]) * multiplication_factors[0]
            y = np.abs(450 - current_data[:,1]) * multiplication_factors[1]
            z = current_data[:,6] / (8766*3600)
            scat = axis.scatter(x, y, c=z, s=2, cmap="viridis_r")
            cbar = plt.colorbar(scat)
            if kwargs.get("cbar_label"):
                cbar.set_label(kwargs.get("cbar_label"))
        
        axis.tick_params(direction="in")
        axis.ticklabel_format(useOffset=False)
        return current_data[np.argmax(current_data[:,6])]
