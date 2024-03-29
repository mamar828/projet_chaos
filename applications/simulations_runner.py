from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

from src.systems.base_system import BaseSystem
from src.bodies.gravitational_body import GravitationalBody
from src.tools.vector import Vector
from src.simulator.simulation_mother import SimulationMother
from src.simulator.simulation import Simulation



if __name__ == '__main__':
    sim_system = BaseSystem(
        list_of_bodies=[GravitationalBody(position=Vector(450,450,0), mass=1.989e30, fixed=True,
                                          integrator="synchronous"),
                        GravitationalBody(position=Vector(300,450,0), velocity=Vector(0,30e-6,0), mass=5.972e27,
                                          fixed=False, integrator="synchronous")],
        n=9
    )

    mommy = SimulationMother(base_system=sim_system)
    foldername = mommy.dispatch(
        simulation_count=400,
        delta_time=5000,
        bodies_per_simulation=50,
        body_initial_position_limits=[(280, 320), (430, 470), (0, 0)],
        body_initial_velocity_limits=[(-50e-6, 50e-6), (-50e-6, 50e-6), (0, 0)],
        save_foldername=f"simulations/double_body",
        simulation_duration=3e8,
        positions_saving_frequency=1,
        potential_gradient_limit= 5e-10,
        body_position_limits=(250,650)
    )
