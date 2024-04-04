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
    # bb = Simulation.load_from_folder("simulations/L1_2").system.get_best_body()

    mommy = SimulationMother(base_system=sim_system)
    foldername = mommy.dispatch(
        simulation_count=1,
        bodies_per_simulation=1,
        delta_time=5000,
        # body_initial_position_limits=[(bb.initial_position.x*0.9999, bb.initial_position.x*1.0001),
        #                               (bb.initial_position.y*0.9999, bb.initial_position.y*1.0001), (0, 0)],
        # body_initial_velocity_limits=[(bb.initial_velocity.x*0.9999, bb.initial_velocity.x*1.0001),
        #                               (bb.initial_velocity.y*0.9999, bb.initial_velocity.y*1.0001), (0, 0)],
        body_initial_position_limits=[(earth.position.x+1.5-0.2, earth.position.x+1.5+0.2),
                                      (earth.position.y-0.1,     earth.position.y+0.1), (0, 0)],
        body_initial_velocity_limits=[(earth.velocity.x-1e-7,    earth.velocity.x+1e-7),
                                      (earth.velocity.y-3e-7,    earth.velocity.y+3e-7), (0, 0)],
        # body_initial_position_limits=[(earth.position.x-10, earth.position.x+10),
        #                               (earth.position.y-10,     earth.position.y+10), (0, 0)],
        # body_initial_velocity_limits=[(earth.velocity.x-1e-7,    earth.velocity.x+1e-7),
        #                               (earth.velocity.y-3e-7,    earth.velocity.y+3e-7), (0, 0)],
        save_foldername=f"simulations/thrash",
        simulation_duration=1e8,
        positions_saving_frequency=1,
        # potential_gradient_limit=1e-10,
        # body_alive_func=Lambda("lambda x, y, z, t_x, t_y, t_z: (1.2 < ((x-t_x)**2 + (y-t_y)**2)**0.5 < 1.8)", 6)
    )
