from pickle import load, dump
from gzip import open as gzip_open

from src.systems.base_system import BaseSystem
from src.engines.engine_2D.engine import Engine_2D
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

    @staticmethod
    def load_pickle_file(filename: str) -> list:
        """
        Load a .pkl file that has been saved with gzip.

        Parameters
        ----------
        filename : str
            Name of the.pkl file to load.

        Returns
        -------
        contents : list
            List containing the contents of the.pkl file.
        """
        bodies = []
        with gzip_open(filename, "rb") as file:
            while True:
                try:
                    bodies.append(load(file))
                except EOFError:
                    break
        return bodies

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
        for line in info:
            if line.startswith("BaseSystem n:"):
                n = int(line.split(" ")[-1])
            elif line.startswith("positions_saving_frequency:"):
                save_freq = int(line.split(" ")[-1])

        base_system = cls.load_pickle_file(f"{foldername}/base_system.gz")
        bodies = cls.load_pickle_file(f"{foldername}/bodies.gz")
        with gzip_open("test.gz", "wb") as file:
            for body in bodies:
                dump(body, file)
        return cls(system=ComputedSystem(base_system + bodies, n=n, tick_factor=save_freq))

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

    def run(self, duration: int, positions_saving_frequency: int) -> dict:
        """
        Run the simulation.

        Parameters
        ----------
        duration : int
            Duration of the simulation in seconds.
        positions_saving_frequency : int
            Sets the number of steps after which the body's positions will be saved. Defaults to 1000.

        Returns
        -------
        results : dict
            Dictionary containing the results of the simulation.
        """
        total_iterations = duration // self.maximum_delta_time
        system = self.system
        for i in range(int(total_iterations // positions_saving_frequency)):
            for i in range(int(positions_saving_frequency)):
                system.update(self.maximum_delta_time)
            # Check for dead bodies in the system
            system.remove_dead_bodies()
            if len(system.attractive_bodies) - len(system.fixed_bodies) == len(system.moving_bodies):
                # Check if no bodies remain
                break
            system.save_positions()
        return {
            "alive": [body for body in system.list_of_bodies if body not in system.attractive_bodies 
                                                            and body not in system.dead_bodies],
            "dead": system.dead_bodies
        }
