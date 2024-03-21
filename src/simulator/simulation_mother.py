import numpy as np

from pickle import dump
from gzip import open as gzip_open
from multiprocessing import Pool
from datetime import datetime, timedelta
from os.path import exists
from os import makedirs
from eztcolors import Colors as C

from src.simulator.simulation import Simulation
from src.systems.base_system import BaseSystem
from src.bodies.gravitational_body import GravitationalBody
from src.bodies.computed_body import ComputedBody
from src.tools.vector import Vector


class Simulation_mother:
    def __init__(self, base_system: BaseSystem, delta_time: float=100):
        self.initial_system = base_system
        self.delta_time = delta_time

    @staticmethod
    def save_results(results: list, save_foldername: str):
        """
        Save the results of a single simulation to a .pkl file.

        Parameters
        ----------
        results : list
            List of dictionaries containing the results of each simulation.
        save_foldername : str
            Name of the folder in which to save the results.
        """
        with gzip_open(f"{save_foldername}/bodies.gz", "wb") as file:
            for listi in results:
                for key, value in listi.items():
                    for body in value:
                        dump(
                            ComputedBody(
                                positions=body.positions,
                                type=key,
                                mass=body.mass,
                                position=body.initial_position,
                                velocity=body.initial_velocity,
                                fixed=body.fixed,
                                has_potential=body.has_potential
                            ), file
                        )

    def save_simulation_parameters(self,
            number_of_processes: int,
            real_time_duration: timedelta,
            positions_saving_frequency: int,
            simulation_duration: int,
            save_foldername: str
        ):
        """
        Save the simulation parameters used by the dispatch method to a file.

        Parameters
        ----------
        number_of_processes : int
            Number of processes used to run the simulation.
        real_time_duration : timedelta
            Duration of the simulation.
        positions_saving_frequency : int
            Frequency at which the bodies' positions were saved.
        simulation_duration : int
            Duration limit of the simulation.
        save_foldername : str
            Name of the folder in which to save the results.
        """
        # The results list is in the form:
        # [{"alive_bodies": [body_objects], "dead_bodies": [body_objets]}, {...}, ...]
        filename_info = f"{save_foldername}/info.txt"
        filename_base = f"{save_foldername}/base_system.gz"

        with open(filename_info, 'w') as file:
            file.write(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write(f"Number of processes: {number_of_processes}\n")
            file.write(f"Real time duration: {real_time_duration}\n")
            file.write(f"Delta time: {self.delta_time}\n")
            file.write(f"Simulation duration: {int(simulation_duration)}\n")
            file.write(f"BaseSystem n: {self.initial_system.n}\n")
            file.write(f"positions_saving_frequency: {int(positions_saving_frequency)}\n")
            file.write(f"alive_position_threshold: {self.initial_system.list_of_bodies[0].alive_position_threshold}\n")
            file.write(f"alive_velocity_threshold: {self.initial_system.list_of_bodies[0].alive_velocity_threshold}")
        
        with gzip_open(filename_base, 'wb') as file:
            for body in self.initial_system.list_of_bodies:
                dump(
                    ComputedBody(
                        positions=body.positions,
                        type="base_body",
                        mass=body.mass,
                        position=body.initial_position,
                        velocity=body.initial_velocity,
                        fixed=body.fixed,
                        has_potential=body.has_potential
                    ), file
                )

    def dispatch(self,
        simulation_count: int,
        bodies_per_simulation: int,
        body_position_limits: list[tuple[float, float]],
        body_velocity_limits: list[tuple[float, float]],
        save_foldername: str,
        simulation_duration: float=1e9,
        positions_saving_frequency: int=1e2
    ) -> str:
        """
        Start a simulation and dispatch to Simulation objects.

        Parameters
        ----------
        simulation_count : int
            The number of simulations to run.
        bodies_per_simulation : int
            Number of bodies to add to each simulation.
        body_position_limits : list[tuple[float, float]]
            Coordinate limits for each body placed in the simulation. The format is [(x_min, x_max), (y_min, y_max),
            (z_min, z_max)].
        body_velocity_limits : list[tuple[float, float]]
            Velocity limits for each body placed in the simulation. The format is [(v_x_min, v_x_max),
            (v_y_min, v_y_max), (v_z_min, v_z_max)].
        save_foldername : str
            Folder in which to save the simulation results.
        simulation_duration : float
            Duration of the simulation in seconds. Defaults to 1e9 seconds. Use multiples of 10 for better results.
        positions_saving_frequency : int
            Sets the number of steps after which the body's positions will be saved. Defaults to 1e2. Use multiples of
            10 for better results.
        
        Returns
        -------
        foldername : str
            Actual name of the folder in which the simulation results were saved.
        """
        while exists(save_foldername):
            if "_" in save_foldername:
                split = save_foldername.split("_")
                try:
                    save_foldername = f"{'_'.join(split[:-1])}_{int(split[-1])+1}"
                except:
                    save_foldername = f"{save_foldername}_1"
            else:
                save_foldername = f"{save_foldername}_1"

        makedirs(save_foldername)

        body_positions = np.array([
            np.random.uniform(*body_position_limits[0], size=simulation_count),
            np.random.uniform(*body_position_limits[1], size=simulation_count),
            np.random.uniform(*body_position_limits[2], size=simulation_count)
        ]).transpose().tolist()
        body_velocities = np.array([
            np.random.uniform(*body_velocity_limits[0], size=bodies_per_simulation),
            np.random.uniform(*body_velocity_limits[1], size=bodies_per_simulation),
            np.random.uniform(*body_velocity_limits[2], size=bodies_per_simulation)
        ]).transpose().tolist()

        print(f"{C.YELLOW}{C.BOLD}Simulation starting at {datetime.now().strftime('%H:%M:%S')} with parameters:" +
              C.END + C.YELLOW +
              f"\n\tsimulation_count:           {simulation_count}" +
              f"\n\tbodies_per_simulation:      {bodies_per_simulation}" +
              f"\n\tbody_position_limits:       {body_position_limits}" +
              f"\n\tbody_velocity_limits:       {body_velocity_limits}" +
              f"\n\tsystem_n:                   {self.initial_system.n}" +
              f"\n\tsimulation_duration:        {simulation_duration:.0e}" +
              f"\n\tpositions_saving_frequency: {positions_saving_frequency:.0e}" +
              f"\n\tsave_foldername:            {save_foldername}{C.END}\n")

        pool = Pool()
        number_of_processes = pool._processes
        print(f"{C.YELLOW}Number of processes used: {number_of_processes}{C.END}")
        start = datetime.now()

        worker_args = [(body_pos, body_velocities, self.initial_system,
                        self.delta_time, simulation_duration, positions_saving_frequency)
                       for body_pos in body_positions]

        results = pool.starmap(worker_simulation, worker_args)
        stop = datetime.now()
        pool.close()
        time = stop - start
        print(f"\n{C.GREEN}Simulation finished in {time}.{C.END}")
        self.save_simulation_parameters(number_of_processes, time, positions_saving_frequency,
                                        simulation_duration, save_foldername)
        self.save_results(results, save_foldername)
        print(f"{C.GREEN+C.BOLD}Simulation successfully saved at {save_foldername}.{C.END}")
        return save_foldername


def worker_simulation(
        body_position: list,
        body_velocities: list[list[float]],
        system: BaseSystem,
        delta_time: float,
        simulation_duration: float,
        positions_saving_frequency: int
    ):
    simulated_system = BaseSystem(
        list_of_bodies=(
            system.list_of_bodies + [GravitationalBody(
                mass=1,
                position=Vector(*body_position),
                velocity=Vector(v_x,v_y,v_z),
                has_potential=False
            ) for v_x, v_y, v_z in body_velocities]
        ),
        n=system.n
    )
    simulation = Simulation(
        system=simulated_system,
        maximum_delta_time=delta_time
    )
    results = simulation.run(simulation_duration, positions_saving_frequency)
    print(".", end="", flush=True)
    return results
