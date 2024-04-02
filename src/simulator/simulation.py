from pickle import load
from gzip import open as gzip_open

from src.systems.base_system import BaseSystem
from src.engines.engine_2D.engine import Engine2D
from src.engines.engine_3D.engine import Engine3D
from src.systems.computed_system import ComputedSystem
from src.engines.engine_3D.elements import Function3D


class Simulation:
    def __init__(self, system: BaseSystem, maximum_delta_time: int=5000):
        """
        Initialize a Simulation object.

        Parameters
        ----------
        system : BaseSystem
            System on which to base the simulation. If a simulation is to be only computed, contains the reference
            bodies but not the added bodies.
        maximum_delta_time : int
            Maximum delta time in seconds accepted for the simulation's time steps. Defaults to 5000.
        """
        self.system = system
        self.maximum_delta_time = maximum_delta_time
        self.traces = None

    def __str__(self):
        returnstr = f"Number of bodies: {len(self.system.list_of_bodies)}\n"
        for body in self.system.list_of_bodies:
            returnstr += str(body) + "\n"
        return returnstr

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
            if line.startswith("BaseSystem n"):
                n = int(line.split(" ")[-1])
            elif line.startswith("positions_saving_frequency"):
                save_freq = int(line.split(" ")[-1])
            elif line.startswith("delta_time"):
                delta_time = int(line.split(" ")[-1])
        
        base_system = cls.load_pickle_file(f"{foldername}/base_system.gz")
        bodies = cls.load_pickle_file(f"{foldername}/bodies.gz")

        return cls(system=ComputedSystem(base_system + bodies, n=n, tick_factor=save_freq*delta_time),
                   maximum_delta_time=delta_time)

    def show_2D(self, *args, traces: list | bool=None, **kwargs):
        """
        Show a simulation in 2D with pygame.

        Parameters
        ----------
        args : list
            Parameters to pass to the Engine2D class.
        traces : list or bool
            Optional, specify the bodies which should leave a trace. If traces is a list of booleans, this controls the
            trace generation of each body in the provided system, in the same order as the bodies in the system. If
            traces is a boolean, all bodies in the system will be traced. Defaults to None.
        kwargs : dict
            Parameters to pass to the Engine2D class.
        """
        if isinstance(traces, bool) and traces:
            self.traces = [True for i in range(len(self.system.list_of_bodies))]
        elif not traces or len(traces) != len(self.system.list_of_bodies):
            self.traces = [None for i in range(len(self.system.list_of_bodies))]
        else:
            self.traces = traces
        app = Engine2D(
            simulation=self,
            *args,
            **kwargs
        )
        app.run()

    def show_3D(self, *args, show_potential: bool=False, **kwargs):
        """
        Show a simulation in 3D with pygame and moderngl.

        Parameters
        ----------
        args : list
            Parameters to pass to the Engine3D class.
        show_potential : bool
            If True, the potential function is passed directly to the Engine3D class. This eases the plotting of the 
            potential field. Defaults to False.
        kwargs : dict
            Parameters to pass to the Engine3D class.
        """
        if show_potential:
            if "functions" in kwargs.keys():
                kwargs["functions"].append(Function3D(
                    texture="spacetime",
                    position=(0,0,0),
                    resolution=(200,200),
                    x_limits=(0,900),
                    y_limits=(0,900),
                    instance=self.system
                ))
            else:
                kwargs["functions"] = [Function3D(
                    texture="spacetime",
                    position=(0,0,0),
                    resolution=(200,200),
                    x_limits=(0,900),
                    y_limits=(0,900),
                    instance=self.system
                )]

        app = Engine3D(
            simulation=self,
            *args,
            **kwargs
        )
        app.run()

    def run(
            self,
            duration: int,
            positions_saving_frequency: int,
            potential_gradient_limit: int,
            body_position_limits: int
        ) -> dict:
        """
        Run the simulation.

        Parameters
        ----------
        duration : int
            Duration of the simulation in seconds.
        positions_saving_frequency : int
            Sets the number of steps after which the body's positions will be saved. Defaults to 1000.
        potential_gradient_limit: int
            Limit for the potential gradient on a body to be considered still alive.
        body_position_limits: tuple[int,int]
            Specify the position in pixels of a body to be considered still alive.

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
            system.remove_dead_bodies(potential_gradient_limit, body_position_limits)
            if len(system.attractive_bodies) - len(system.fixed_bodies) == len(system.moving_bodies):
                # Check if no bodies remain
                break
            system.save_positions()
        return {
            "alive": [body for body in system.list_of_bodies if body not in system.attractive_bodies 
                                                            and body not in system.dead_bodies],
            "dead": system.dead_bodies,
        }
    
    def run_attractive_bodies(self, duration: int, positions_saving_frequency: int) -> list:
        """ 
        Run the simulation only for the attractive moving bodies of the system.

        Parameters
        ----------
        duration : int
            Duration of the simulation in seconds.
        positions_saving_frequency : int
            Sets the number of steps after which the body's positions will be saved. Defaults to 1000.

        Returns
        -------
        results : dict
            The body objects with their positions attributes completed. Contains only the "attractive_moving" keyword.
        """
        total_iterations = duration // self.maximum_delta_time
        system = self.system
        for i in range(int(total_iterations // positions_saving_frequency)):
            for i in range(int(positions_saving_frequency)):
                system.update(self.maximum_delta_time)
            system.save_positions()
        return {"attractive_moving": [body for body in system.list_of_bodies if body in system.moving_bodies]}
