import numpy as np

from multiprocessing import Pool
from datetime import datetime, timedelta
from os.path import exists
from os import makedirs
from pandas import DataFrame
from eztcolors import Colors as C

from src.simulator.simulation import Simulation
from src.systems.base_system import BaseSystem
from src.bodies.gravitational_body import GravitationalBody
from src.tools.vector import Vector


class Simulation_mother:
    def __init__(self, base_system: BaseSystem, delta_time: float=100):
        self.initial_system = base_system
        self.delta_time = delta_time

    def save_results(self, results: list, number_of_processes: int, duration_time: timedelta, save_foldername: str):
        """
        Save the results outputted by the dispatch method to a file.

        Parameters
        ----------
        results : list
            List of dictionaries containing the results of each simulation.
        number_of_processes : int
            Number of processes used to run the simulation.
        duration_time : timedelta
            Duration of the simulation.
        save_foldername : str
            Name of the folder in which to save the results.
        """
        # The results list is in the form:
        # [{"alive_bodies": [body_objects], "dead_bodies": [body_objets]}, {...}, ...]
        filename_0 = f"{save_foldername}/info.txt"
        filename_1 = f"{save_foldername}/base_system.csv"
        filename_2 = f"{save_foldername}/bodies.csv"

        header_1 = ["fixed", "mass", "initial_position", "initial_velocity", "positions"]
        header_2 = ["state", "initial_position", "initial_velocity", "positions"]

        data_1 = []
        for body in self.initial_system.list_of_bodies:
            data_1.append([body.fixed, body.mass, body.initial_position, body.initial_velocity, body.positions])

        data_2 = []
        for dicti in results:
            for key, value in dicti.items():
                for body in value:
                    data_2.append([key.split("_")[0], body.initial_position, body.initial_velocity, body.positions])

        makedirs(save_foldername)

        with open(filename_0, 'w') as file:
            file.write(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write(f"Number of processes: {number_of_processes}\n")
            file.write(f"Duration: {duration_time}\n")
            file.write(f"Delta time: {self.delta_time}\n")
            file.write(f"BaseSystem n: {self.initial_system.n}\n")
            if results[0]["alive_bodies"]:
                file.write(f"alive_position_threshold: {results[0]['alive_bodies'][0].alive_position_threshold}\n")
                file.write(f"alive_velocity_threshold: {results[0]['alive_bodies'][0].alive_velocity_threshold}\n")
            elif results[0]["dead_bodies"]:
                file.write(f"alive_position_threshold: {results[0]['dead_bodies'][0].alive_position_threshold}\n")
                file.write(f"alive_velocity_threshold: {results[0]['dead_bodies'][0].alive_velocity_threshold}\n")
            else:
                file.write(f"Error: alive and dead lists are empty.\n")
                file.write(f"Error: alive and dead lists are empty.\n")
        
        DataFrame(data_1, columns=header_1).to_csv(filename_1, index=False)
        DataFrame(data_2, columns=header_2).to_csv(filename_2, index=False)
        print(f"{C.GREEN+C.BOLD}Simulation successfully saved at {save_foldername}.{C.END}")

    def dispatch(self,
            simulation_count: int,
            bodies_per_simulation: int,
            body_position_limits: list[tuple[float, float]],
            body_velocity_limits: list[tuple[float, float]],
            save_foldername: str,
            simulation_duration: float=1e9
    ):
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
            Duration of the simulation in seconds. Defaults to 1e9 seconds.
        """
        # assert not exists(save_foldername), (f"{C.RED+C.BOLD}{save_foldername} already exists, please choose " +
        #                                      f"a different name.{C.END}")
        while exists(save_foldername):
            if "_" in save_foldername:
                split = save_foldername.split("_")
                try:
                    save_foldername = f"{'_'.join(split[:-1])}_{int(split[-1])+1}"
                except:
                    save_foldername = f"{save_foldername}_1"
            else:
                save_foldername = f"{save_foldername}_1"

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
              f"\n\tSimulation_count:      {simulation_count}" +
              f"\n\tBodies_per_simulation: {bodies_per_simulation}" +
              f"\n\tBody position limits:  {body_position_limits}" +
              f"\n\tBody velocity limits:  {body_velocity_limits}" +
              f"\n\tSystem n:              {self.initial_system.n}" +
              f"\n\tSimulation duration:   {simulation_duration}" +
              f"\n\tSave foldername:       {save_foldername}{C.END}\n")
        
        pool = Pool()
        number_of_processes = pool._processes
        print(f"{C.YELLOW}Number of processes used: {number_of_processes}{C.END}")
        start = datetime.now()

        worker_args = [(body_pos, body_velocities, self.initial_system, self.delta_time, simulation_duration) 
                       for body_pos in body_positions]

        results = pool.starmap(worker_simulation, worker_args)
        stop = datetime.now()
        pool.close()
        time = stop - start
        print(f"\n{C.GREEN}Simulation finished in {time}.{C.END}")
        self.save_results(results, number_of_processes, time, save_foldername)


def worker_simulation(
        body_position: list,
        body_velocities: list[list[float]],
        system: BaseSystem,
        delta_time: float,
        simulation_duration: float
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
    results = simulation.run(simulation_duration)
    print(".", end="", flush=True)
    return results
