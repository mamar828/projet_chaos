from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

from astropy.constants import M_sun, M_earth

from src.systems.base_system import BaseSystem
from src.bodies.gravitational_body import GravitationalBody
from src.tools.vector import Vector
from src.simulator.simulation_mother import SimulationMother
from src.simulator.simulation import Simulation
from src.simulator.lambda_func import Lambda



if __name__ == '__main__':
    sun = GravitationalBody(mass=M_sun.value, position=Vector(450,450,0), fixed=True)
    earth = GravitationalBody(mass=M_earth.value, position=Vector(297.90,450,0),
                              velocity=Vector(0,-29.29e-6,0), fixed=False) # Parameters at apoapsis
    sim_system = BaseSystem(list_of_bodies=[sun, earth], n=9)
    mommy = SimulationMother(base_system=sim_system)
    foldername = mommy.dispatch(
        simulation_count=1000,
        delta_time=5000,
        bodies_per_simulation=100,
        body_initial_position_limits=[(round(earth.position.x+1.5-0.2,10), round(earth.position.x+1.5+0.2,10)),
                                      (round(earth.position.y-0.1,10), round(earth.position.y+0.1,10)), (0, 0)],
        body_initial_velocity_limits=[(round(earth.velocity.x-1e-7,10), round(earth.velocity.x+1e-7,10)),
                                      (round(earth.velocity.y-3e-7,10), round(earth.velocity.y+3e-7,10)), (0, 0)],
        save_foldername=f"simulations/L1_1",
        simulation_duration=5e8,
        positions_saving_frequency=10,
        potential_gradient_limit=1e-11,
        body_alive_func=Lambda("lambda x, y, z, t_x, t_y, t_z: (1.2 < ((x-t_x)**2 + (y-t_y)**2)**0.5 < 1.8)", 6)
        # body_alive_limits=(
        #     Lambda(lambda x, tracked_body: abs(tracked_body.position.x - x) < 2),
        #     Lambda(lambda y, tracked_body: abs(tracked_body.position.y - y) < 2),
        #     None
        # )
    )
