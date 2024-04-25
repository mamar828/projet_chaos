from __future__ import annotations

from pickle import load
from gzip import open as gzip_open
from os.path import exists
from eztcolors import Colors as C

from src.systems.base_system import BaseSystem
from src.systems.computed_system import ComputedSystem
from src.engines.engine_3D.elements import Function3D
from src.simulator.lambda_func import Lambda
try:
    from src.engines.engine_2D.engine import Engine2D
    from src.engines.engine_3D.engine import Engine3D
except ImportError:
    Engine2D = None
    Engine3D = None

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
        return f"Number of bodies: {len(self.system.list_of_bodies)}\n" + \
                "\n".join([str(body) for body in self.system.list_of_bodies])

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
    def load_from_folder(
            cls,
            foldername: str,
            min_time_survived: int=None,
            only_load_best_body: bool=False
        ) -> Simulation:
        """
        Load a simulation from a folder containing details of a previously rendered simulation.

        Parameters
        ----------
        foldername : str
            Name of the folder containing the simulation details.
        min_time_survived : int
            Minimum time a body survived to be displayed. Defaults to None.
        only_load_best_body : bool
            Whether the simulation should only be loaded with the best body. If False, all the bodies will be loaded.
            Defaults to False.

        Returns
        -------
        simulation : Simulation
            Simulation object with the precomputed system.
        """
        assert exists(foldername), f"{C.RED+C.BOLD}Provided foldername ({foldername}) does not exist.{C.END}"
        info = open(f"{foldername}/info.txt", "r").readlines()
        info_dict = {}
        for line in info:
            split = line.split(":")
            info_dict[split[0]] = ":".join(split[1:])[1:-1]
        n = float(info_dict["BaseSystem n"])
        save_freq = float(info_dict["positions_saving_frequency"])
        delta_time = float(info_dict["delta_time"])
        
        base_system = cls.load_pickle_file(f"{foldername}/base_system.gz")
        if only_load_best_body:
            bodies = cls.load_pickle_file(f"{foldername}/best_body.gz")
        else:
            bodies = cls.load_pickle_file(f"{foldername}/bodies.gz")

        if min_time_survived and not only_load_best_body:
            bodies = [body for body in bodies if body.time_survived >= min_time_survived]

        return cls(system=ComputedSystem(base_system + bodies, n=n, tick_factor=save_freq*delta_time, info=info_dict),
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

    def show_3D(self, show_potential: bool=False, **kwargs):
        """
        Show a simulation in 3D with pygame and moderngl.

        Parameters
        ----------
        show_potential : bool
            If True, the potential function is passed directly to the Engine3D class. This eases the plotting of the 
            potential field. Defaults to False.
        kwargs : dict
            Parameters to pass to the Engine3D class.
        """
        if show_potential:
            kwargs["functions"] = kwargs.get("functions", []) + [
                Function3D(
                    texture="spacetime",
                    position=(0,0,0),
                    resolution=(200,200),
                    x_limits=(0,900),
                    y_limits=(0,900),
                    instance=self.system
                )
            ]

        app = Engine3D(
            simulation=self,
            **kwargs
        )
        app.run()

    def run(
            self,
            duration: int,
            positions_saving_frequency: int,
            potential_gradient_limit: float,
            body_alive_func: Lambda
        ) -> dict:
        """
        Run the simulation.

        Parameters
        ----------
        duration : int
            Duration of the simulation in seconds.
        positions_saving_frequency : int
            Sets the number of steps after which the body's positions will be saved.
        potential_gradient_limit: float
            Limit for the potential gradient on a body to be considered still alive.
        body_alive_func: Lambda
            Lambda function specifying the conditions a body must respect to stay alive.

        Returns
        -------
        results : dict
            Results of the simulation. The keys "alive" and "dead" provide the corresponding bodies, in the form of a
            list.
        """
        total_iterations = duration // self.maximum_delta_time
        system = self.system
        system.method = "force"
        dead_body_removal_frequency = 10
        for i in range(1, int(total_iterations // positions_saving_frequency)+1):
            for j in range(int(positions_saving_frequency)):
                system.update(self.maximum_delta_time)

                if (i * positions_saving_frequency + j) % dead_body_removal_frequency == 0:
                    # Check for dead bodies in the system
                    system.remove_dead_bodies(potential_gradient_limit, body_alive_func)

            # Check if no bodies remain
            if len(system.attractive_bodies) - len(system.fixed_bodies) == len(system.moving_bodies):
                break
            
            system.save_positions()
        
        return {
            "alive": [body for body in system.moving_bodies if body not in system.attractive_bodies],
            "dead": system.dead_bodies
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
        system.method = "force"
        for i in range(int(total_iterations // positions_saving_frequency)):
            for i in range(int(positions_saving_frequency)):
                system.update(self.maximum_delta_time)
            system.save_positions(save_fake=True)
        return {
            "attractive_moving": [body for body in system.list_of_bodies if body in system.moving_bodies],
            "fake": system.fake_bodies[0]
        }
    