import numpy as np

from pickle import dump
from gzip import open as gzip_open
from gzip import GzipFile
from multiprocessing import Pool
from datetime import datetime
from os.path import exists
from os import makedirs
from tqdm import tqdm
from typing import Callable
from eztcolors import Colors as C

from src.simulator.simulation import Simulation
from src.simulator.lambda_func import Lambda
from src.systems.base_system import BaseSystem
from src.systems.new_system import NewSystem
from src.bodies.gravitational_body import GravitationalBody
from src.bodies.fake_body import FakeBody
from src.bodies.new_body import NewBody
from src.bodies.computed_body import ComputedBody
from src.tools.vector import Vector


class SimulationMother:
    def __init__(self, base_system: BaseSystem):
        self.initial_system = base_system
        self.pool = None

    @staticmethod
    def dump_body(body: GravitationalBody | ComputedBody | FakeBody, type: str, file: GzipFile):
        """
        Dump a body of a certain type into a file.

        Parameters
        ----------
        body : GravitationalBody | ComputedBody
            Body to dump into the file.
        type : str
            Type of the body.
        file : gzip.GzipFile
            Reference to the file in which the body should be dumped.
        """
        dump(
            ComputedBody(
                positions=body.positions,
                type=type,
                mass=body.mass,
                position=body.initial_position,
                velocity=body.initial_velocity,
                fixed=body.fixed,
                has_potential=body.has_potential,
                integrator=body.integrator,
                time_survived=body.time_survived
            ), file
        )

    def save_results(self, results: list, save_foldername: str):
        """
        Save the results of a single simulation to a .pkl file.

        Parameters
        ----------
        results : list
            List of dictionaries containing the results of each simulation.
        save_foldername : str
            Name of the folder in which to save the results.
        """
        print(C.LIGHT_CYAN, end="")
        fake_body_saved = False
        with gzip_open(f"{save_foldername}/bodies.gz", "wb") as file:
            for listi in tqdm(results, desc="Saving", miniters=1, mininterval=0.001):
                for key, value in listi.items():
                    if key == "fake":
                        body = value
                        if fake_body_saved:
                            continue
                        else:
                            self.dump_body(body, body.type, file)
                            fake_body_saved = True
                    else:
                        for body in value:
                            self.dump_body(body, key, file)
        print(C.END, end="")

    def save_best_body(self, results: list, save_foldername: str) -> int:
        """ 
        Save in its own file the body that has survived the longest during simulating. Also returns the time survived.

        Parameters
        ----------
        results : list
            List of dictionaries containing the results of each simulation.
        save_foldername : str
            Name of the folder in which to save the results.
        
        Returns
        -------
        max_time_survived : int
            Maximum time survived.
        """
        max_number = 0
        max_body = None
        body_type = "dead"
        for listi in results[1:]:           # Remove first value has it corresponds to the attractive body simulation
            for state, bodies in listi.items():
                if state == "alive" and bodies:
                    max_number = bodies[0].time_survived
                    max_body = bodies[0]
                    body_type = "alive"
                    break
                else:
                    for body in bodies:
                        if body.time_survived > max_number:
                            max_number = body.time_survived
                            max_body = body
            else:
                continue
            break

        if max_body:
            with gzip_open(f"{save_foldername}/best_body.gz", "wb") as file:
                # Save attractive moving bodies
                attractive_moving = results[0].get("attractive_moving")
                if attractive_moving:
                    for body in attractive_moving:
                        self.dump_body(body, "attractive_moving", file)
                if results[0]["fake"]:
                    self.dump_body(results[0]["fake"], results[0]["fake"].type, file)
                self.dump_body(max_body, body_type, file)
        return max_number

    def save_simulation_parameters(self, save_foldername: str, **kwargs):
        """
        Save the simulation parameters used by the dispatch method to a file.

        Parameters
        ----------
        save_foldername : str
            Name of the folder in which to save the results.
        kwargs : dict
            Every element to be saved to the info file. Saves in the form key: value.
        """
        filename_info = f"{save_foldername}/info.txt"
        filename_base = f"{save_foldername}/base_system.gz"

        with open(filename_info, 'w') as file:
            file.write(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write(f"BaseSystem n: {self.initial_system.n}\n")
            for key, value in kwargs.items():
                file.write(f"{key}: {value}\n")
        
        with gzip_open(filename_base, 'wb') as file:
            for body in self.initial_system.list_of_bodies:
                if body.fixed:
                    self.dump_body(body, "base_body", file)

    def dispatch(
            self,
            simulation_count: int,
            bodies_per_simulation: int,
            body_initial_position_limits: list[tuple[float, float]],
            body_initial_velocity_limits: list[tuple[float, float]],
            save_foldername: str,
            simulation_duration: float=1e8,
            delta_time: float=5000,
            positions_saving_frequency: int=1e2,
            potential_gradient_limit: float=5e-10,
            body_alive_func: Lambda=Lambda("lambda x,y,z: (0 < x < 900) and (0 < y < 900)", 3),
            integrator: str="synchronous"
        ) -> str:
        """
        Start a simulation and dispatch to Simulation objects.

        Parameters
        ----------
        simulation_count : int
            The number of simulations to run.
        bodies_per_simulation : int
            Number of bodies to add to each simulation.
        body_initial_position_limits : list[tuple[float, float]]
            Coordinate limits for each body placed in the simulation. The format is [(x_min, x_max), (y_min, y_max),
            (z_min, z_max)].
        body_initial_velocity_limits : list[tuple[float, float]]
            Velocity limits for each body placed in the simulation. The format is [(v_x_min, v_x_max),
            (v_y_min, v_y_max), (v_z_min, v_z_max)].
        save_foldername : str
            Folder in which to save the simulation results.
        simulation_duration : float
            Duration of the simulation in seconds. Defaults to 1e8 seconds (≈ 3 years). Use multiples of 10 for better
            results.
        delta_time : float
            Delta time between of each step. Defaults to 1000.
        positions_saving_frequency : int
            Sets the number of steps after which the body's positions will be saved. Defaults to 1e2. Use multiples of
            10 for better results. Also sets the frequency at which the bodies' state will be checked (dead/alive)
        potential_gradient_limit: float
            Limit for the potential gradient on a body to be considered still alive. Defaults to 5e-10.
        body_alive_func: Lambda
            Lambda function specifying the conditions a body must respect to stay alive. Defaults to :
            Lambda("lambda x,y,z: (0<x<900) and (0<y<900)", 3), which only keeps body's whose x and y values are
            between 0 and 900.
        integrator : str
            Integrator to use for computing the body positions. Supported integrators can be found in 
            src.bodies.gravitational_bodies.__call__. Defaults to "synchronous".
        
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

        if not potential_gradient_limit: potential_gradient_limit = 1e10
        
        body_initial_position_limits = [(round(val[0],10), round(val[1],10)) for val in body_initial_position_limits]
        body_initial_velocity_limits = [(round(val[0],10), round(val[1],10)) for val in body_initial_velocity_limits]

        def get_meshed_array(x_lims, y_lims, z_lims, count) -> np.ndarray:
            x_coords = np.linspace(*x_lims, num=round(count**(1/3)))
            y_coords = np.linspace(*y_lims, num=round(count**(1/3)))
            z_coords = np.linspace(*z_lims, num=round(count**(1/3)))
            X, Y, Z = np.meshgrid(x_coords, y_coords, z_coords)
            return np.vstack((X.ravel(), Y.ravel(), Z.ravel())).transpose()

        if True:
            body_positions = np.array([
                np.random.uniform(*body_initial_position_limits[0], size=simulation_count),
                np.random.uniform(*body_initial_position_limits[1], size=simulation_count),
                np.random.uniform(*body_initial_position_limits[2], size=simulation_count)
            ]).transpose()
            body_velocities = np.array([
                np.random.uniform(*body_initial_velocity_limits[0], size=bodies_per_simulation),
                np.random.uniform(*body_initial_velocity_limits[1], size=bodies_per_simulation),
                np.random.uniform(*body_initial_velocity_limits[2], size=bodies_per_simulation)
            ]).transpose().tolist()
        elif False:
            body_positions = np.array([
                np.tile(np.linspace(*body_initial_position_limits[0], num=int(simulation_count**0.5)),
                        int(simulation_count**0.5)),
                np.repeat(np.linspace(*body_initial_position_limits[1], num=int(simulation_count**0.5)),
                        int(simulation_count**0.5)),
                np.linspace(*body_initial_position_limits[2], num=simulation_count)
            ]).transpose().tolist()
            body_velocities = np.array([
                np.tile(np.linspace(*body_initial_velocity_limits[0], num=int(bodies_per_simulation**0.5)),
                        int(bodies_per_simulation**0.5)),
                np.repeat(np.linspace(*body_initial_velocity_limits[1], num=int(bodies_per_simulation**0.5)),
                        int(bodies_per_simulation**0.5)),
                np.linspace(*body_initial_velocity_limits[2], num=bodies_per_simulation)
            ]).transpose().tolist()
        else:
            body_positions = get_meshed_array(*body_initial_position_limits, simulation_count).tolist()
            body_velocities = get_meshed_array(*body_initial_velocity_limits, bodies_per_simulation).tolist()

        print(f"{C.YELLOW+C.BOLD}Simulation starting at {datetime.now().strftime('%H:%M:%S')} with parameters:{C.END}")
        print(C.BROWN)
        print(f"\n    simulation_count:         {simulation_count}" +
              f"\n    bodies_per_simulation:    {bodies_per_simulation}" +
              f"\n    delta_time:               {delta_time}" +
              f"\n    body_init_pos_limits:     {body_initial_position_limits}" +
              f"\n    body_init_vel_limits:     {body_initial_velocity_limits}" +
              f"\n    potential_gradient_limit: {potential_gradient_limit:.0e}" +
              f"\n    body_alive_func:          {True if body_alive_func else False}" +
              f"\n    system_n:                 {self.initial_system.n}" +
              f"\n    simulation_duration:      {simulation_duration:.0e}" +
              f"\n    pos_saving_frequency:     {positions_saving_frequency:.0f}" +
              f"\n    integrator:               {integrator}" +
              f"\n    save_foldername:          {save_foldername}{C.END}\n")

        self.pool = Pool()
        number_of_processes = self.pool._processes
        print(f"{C.BROWN}Number of processes used: {number_of_processes}{C.END}")
        start = datetime.now()

        worker_args = [(body_pos, body_velocities, self.initial_system, delta_time, simulation_duration,
                        positions_saving_frequency, potential_gradient_limit, body_alive_func, integrator)
                       for body_pos in body_positions]
        
        # Dispatch a worker simulation to compute the independent movement of attractive moving bodies
        if self.initial_system.moving_bodies:
            special_args = [(None, None, self.initial_system, delta_time, simulation_duration,
                             positions_saving_frequency, None, None, integrator)]
        else:
            special_args = []

        total_args = special_args + worker_args
        results = []
        mapped_pool = self.pool.imap(self.worker_simulation_star, total_args)
        print(C.LIGHT_PURPLE, end="")
        for result in tqdm(mapped_pool, total=len(total_args), desc="Simulating", miniters=1, mininterval=0.001):
            results.append(result)
        print(C.END, end="")
        stop = datetime.now()
        time = stop - start
        print(f"\n{C.GREEN}Simulation finished in {time}.{C.END}")

        makedirs(save_foldername)

        max_time_survived = self.save_best_body(results, save_foldername)
        self.save_simulation_parameters(
            save_foldername, number_of_processes=number_of_processes, real_time_duration=time,
            simulation_count=simulation_count, bodies_per_simulation=bodies_per_simulation,
            body_initial_position_limits=body_initial_position_limits,
            body_initial_velocity_limits=body_initial_velocity_limits,
            positions_saving_frequency=int(positions_saving_frequency),
            simulation_duration=f"{simulation_duration:.3e}",
            delta_time=delta_time, integrator=integrator, potential_gradient_limit=potential_gradient_limit,
            body_alive_func=str(body_alive_func), max_time_survived=f"{max_time_survived:.3e}"
        )
        self.save_results(results, save_foldername)
        print(f"{C.GREEN+C.BOLD}Simulation successfully saved at {save_foldername}.{C.END}")
        self.pool.close()
        return save_foldername
    
    @staticmethod
    def worker_simulation_star(args):
        """
        Makes multiprocessing.pool.map -> multiprocessing.pool.starmap.
        """
        return worker_simulation(*args)


def worker_simulation(
        body_position: list,
        body_velocities: list[list[float]],
        system: BaseSystem,
        delta_time: float,
        simulation_duration: float,
        positions_saving_frequency: int,
        potential_gradient_limit: int,
        body_alive_func: tuple[int,int],
        integrator: str
    ):
    if not isinstance(body_position, np.ndarray) and not isinstance(body_velocities, np.ndarray):
        # Special simulation, occuring only once
        simulation = Simulation(
            system=system,
            maximum_delta_time=delta_time
        )
        result = simulation.run_attractive_bodies(simulation_duration, positions_saving_frequency)

    else:
        # Normal simulation
        simulated_system = BaseSystem(
            list_of_bodies=(
                system.list_of_bodies + [GravitationalBody(
                    mass=1,
                    position=Vector(*body_position),
                    velocity=Vector(v_x,v_y,v_z),
                    has_potential=False,
                    integrator=integrator
                ) for v_x, v_y, v_z in body_velocities]
            ),
            n=system.n
        )
        simulation = Simulation(
            system=simulated_system,
            maximum_delta_time=delta_time
        )
        result = simulation.run(simulation_duration, positions_saving_frequency,
                                potential_gradient_limit, body_alive_func)

    return result
