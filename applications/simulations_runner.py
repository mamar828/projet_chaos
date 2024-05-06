from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

from astropy.constants import M_sun

from src.systems.base_system import BaseSystem
from src.bodies.gravitational_body import GravitationalBody
from src.bodies.fake_body import *
from src.tools.vector import Vector
from src.simulator.simulation_mother import SimulationMother
from src.simulator.simulation import Simulation
from src.simulator.lambda_func import Lambda
from applications.simulations_examples import sun, earth



if __name__ == '__main__':
    sim_system = BaseSystem(list_of_bodies=[sun, earth, L1Body()], n=9)

    mommy = SimulationMother(base_system=sim_system)
    foldername = mommy.dispatch(
        simulation_count=50,
        bodies_per_simulation=10,
        delta_time=5000,
        body_initial_position_limits=[
            (sim_system.fake_bodies[0].position.x-10,  sim_system.fake_bodies[0].position.x+10),
            (sim_system.fake_bodies[0].position.y-10,  sim_system.fake_bodies[0].position.y+10), 
            (0,                                        0)
        ],
        body_initial_velocity_limits=[
            (earth.velocity.x-200e-7,                  earth.velocity.x-300e-7),
            (earth.velocity.y+110e-7,                  earth.velocity.y+170e-7),
            (0,                                        0)
        ],
        save_foldername=f"simulations/L1",
        simulation_duration=3e8,
        integrator="synchronous",
        positions_saving_frequency=1,
        potential_gradient_limit=1e-10,
        body_alive_func=Lambda(
            "lambda x, y, z, t_x, t_y, t_z: -15 < x - t_x < 15 and -15 < y - t_y < 15", 6
        )
    )
