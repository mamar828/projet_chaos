from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

from src.systems.base_system import BaseSystem
from src.bodies.gravitational_body import GravitationalBody
from src.tools.vector import Vector
from src.simulator.simulation_mother import SimulationMother
from src.simulator.simulation import Simulation
from src.simulator.lambda_func import Lambda
from applications.simulations_examples import sun, earth



if __name__ == '__main__':
    other_body = GravitationalBody(
        mass=10,
        position=Vector(earth.position.x+1.5, earth.position.y, 0),
        velocity=Vector(earth.velocity.x, earth.velocity.y, 0),
        has_potential=False,
        integrator="kick-drift-kick"
    )
    sim_system = BaseSystem(list_of_bodies=[sun, earth, other_body], n=9)
    # bb = Simulation.load_from_folder("simulations/L1_2").system.get_best_body()

    sim = Simulation(system=sim_system)
    sim.show_3D(
        show_potential=True,
        model_size_type="realistic",
        # model_size_type="exaggerated",
        window_size=(1440,900),
        # camera_position_mode="following",
        camera_position_mode="free",
        # camera_movement_mode="instantaneous"
        camera_movement_mode="cinematic"
    )
