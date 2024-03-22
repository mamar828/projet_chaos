from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

from src.systems.base_system import BaseSystem
from src.bodies.gravitational_body import GravitationalBody
from src.tools.vector import Vector
from src.simulator.simulation_mother import Simulation_mother



if __name__ == '__main__':
    sim_system = BaseSystem(
        list_of_bodies=[GravitationalBody(position=Vector(250,250,0), mass=1.989e30, fixed=True)],
        n=9
    )

    mommy = Simulation_mother(base_system=sim_system, delta_time=100)
    foldername = mommy.dispatch(
        simulation_count=8,
        bodies_per_simulation=3,
        body_initial_position_limits=[(100, 400), (100, 400), (0, 0)],
        body_initial_velocity_limits=[(-50e-6, 50e-6), (-50e-6, 50e-6), (0, 0)],
        save_foldername=f"simulations/dead_method",
        simulation_duration=1e8,
        positions_saving_frequency=5e2,
        potential_gradient_limit= 5e-10,
        body_position_limits=(0,500)
    )
