from pandas import read_csv

from src.systems.base_system import BaseSystem
from src.engines.engine_2D.engine import Engine_2D
from src.bodies.computed_body import ComputedBody
from src.systems.computed_system import ComputedSystem


class Simulation:
    def __init__(self, system: BaseSystem, maximum_delta_time: float=100):
        """
        Initialize a Simulation object.

        Parameters
        ----------
        system : BaseSystem
            System on which to base the simulation. If a simulation is to be only computed, contains the reference
            bodies but not the added bodies.
        maximum_delta_time : float
            Maximum delta time in seconds accepted for the simulation's time steps.
        """
        self.system = system
        self.maximum_delta_time = maximum_delta_time
        self.traces = None

    @classmethod
    def load_from_folder(cls, foldername: str):
        """
        Load a simulation from a folder containing details of a previously rendered simulation.

        Parameters
        ----------
        foldername : str
            Name of the folder containing the simulation details.
        """
        info = open(f"{foldername}/info.txt", "r").readlines()
        n = info[3].split(" ")[-1]
        base_system = read_csv(f"{foldername}/base_system.csv")
        bodies = read_csv(f"{foldername}/bodies.csv")
        
        list_of_bodies = []
        for i in range(len(base_system)):
            body = base_system.loc[i]
            list_of_bodies.append(
                ComputedBody(
                    positions=body.positions,
                    type="base_body",
                    mass=body.mass,
                    position=body.initial_position,
                    velocity=body.initial_velocity,
                    fixed=body.fixed,
                    has_potential=True
            ))

        for i in range(len(bodies)):
            body = bodies.loc[i]
            list_of_bodies.append(
                ComputedBody(
                    positions=body.positions,
                    type=body.state,
                    mass=1,
                    position=body.initial_position,
                    velocity=body.initial_velocity,
                    fixed=False,
                    has_potential=False
            ))
        
        return cls(system=ComputedSystem(list_of_bodies, n=n))

    def show(self, *args, traces: list=None, **kwargs):
        """
        Show a simulation.

        Parameters
        ----------
        args : list
            Parameters to pass to the Engine_2D class.
        traces : list
            Optional, specify the bodies which should leave a trace.
        kwargs : dict
            Parameters to pass to the Engine_2D class.
        """
        if not traces or len(traces) != len(self.system.list_of_bodies):
            self.traces = [None for i in range(len(self.system.list_of_bodies))]
        else:
            self.traces = traces
        app = Engine_2D(
            simulation=self,
            *args,
            **kwargs
        )
        app.run()

    def run(self, duration) -> dict:
        """
        Run the simulation.

        Parameters
        ----------
        duration : int
            Duration of the simulation in seconds.

        Returns
        -------
        results : dict
            Dictionary containing the results of the simulation.
        """
        total_iterations = duration // self.maximum_delta_time
        system = self.system
        for i in range(int(total_iterations // 100)):
            for i in range(100):
                system.update(self.maximum_delta_time)
            # Check for dead bodies in the system
            system.remove_dead_bodies()
            if len(system.attractive_bodies) - len(system.fixed_bodies) == len(system.moving_bodies):
                # Check if no bodies remain
                break
        return {
            "alive_bodies": [body for body in system.list_of_bodies if body not in system.attractive_bodies],
            "dead_bodies": system.dead_bodies
        }
