from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

from astropy.constants import M_sun, M_earth

from src.systems.base_system import BaseSystem
from src.bodies.gravitational_body import GravitationalBody
from src.tools.vector import Vector
from src.simulator.simulation_mother import SimulationMother
from src.simulator.simulation import Simulation



if __name__ == '__main__':
    sun = GravitationalBody(mass=M_sun.value, position=Vector(450,450,0), fixed=True)
    earth = GravitationalBody(mass=M_earth.value, position=Vector(297.90,450,0),
                              velocity=Vector(0,-29.29e-6,0), fixed=False) # Parameters at apoapsis
    sim_system = BaseSystem(list_of_bodies=[sun, earth], n=9)

    mommy = SimulationMother(base_system=sim_system)
    foldername = mommy.dispatch(
        simulation_count=230,
        delta_time=5000,
        bodies_per_simulation=50,
        body_initial_position_limits=[(earth.position.x+1.5-0.1, earth.position.x+1.5+0.1),
                                      (earth.position.y-0.1, earth.position.y+0.1), (0, 0)],
        body_initial_velocity_limits=[(earth.velocity.x-1e-7, earth.velocity.x+1e-7),
                                      (earth.velocity.y-1e-7, earth.velocity.y+1e-7), (0, 0)],
        save_foldername=f"simulations/L1",
        simulation_duration=3e9,
        positions_saving_frequency=4,
        potential_gradient_limit= 5e-10,
        body_position_limits=(295,605)
    )
