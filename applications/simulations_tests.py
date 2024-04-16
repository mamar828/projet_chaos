from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import numpy as np

from src.systems.base_system import BaseSystem
from src.systems.new_system import NewSystem
from src.bodies.gravitational_body import GravitationalBody
from src.bodies.fake_body import FakeBody
from src.bodies.new_body import NewBody
from src.tools.vector import Vector
from src.simulator.simulation_mother import SimulationMother
from src.simulator.simulation import Simulation
from src.simulator.lambda_func import Lambda
from applications.simulations_examples import sun, earth
from src.engines.engine_3D.elements import Function3D

from astropy.constants import M_sun
sun2 = GravitationalBody(mass=M_sun.value, position=Vector(450,440,0), fixed=True, integrator="synchronous")


if __name__ == '__main__':
    L1 = FakeBody()
    sim_system = BaseSystem(list_of_bodies=[sun, earth, L1], n=9)
    # bb = Simulation.load_from_folder("simulations/L1_2").system.get_best_body()

    sim = Simulation(system=sim_system, maximum_delta_time=5000)
    # sim.run(
    #     duration=1e8,
    #     positions_saving_frequency=10,
    #     potential_gradient_limit=None,
    #     body_alive_func=None
    # )
    # sim.show_2D(traces=True, display_clock=True, window_size=(900,900))
    sim.show_3D(
        show_potential=True,
        model_size_type="realistic",
        # model_size_type="exaggerated",
        window_size=(1440,900),
        camera_movement_mode="instantaneous"
        # camera_movement_mode="cinematic"
    )
