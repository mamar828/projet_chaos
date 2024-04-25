from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import numpy as np

from src.systems.base_system import BaseSystem
from src.systems.new_system import NewSystem
from src.bodies.gravitational_body import GravitationalBody
from src.bodies.fake_body import *
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
    # sim_system = BaseSystem(list_of_bodies=[sun, earth, L1Body(), L2Body(), L3Body(), L4Body(), L5Body()], n=9)
    sim = Simulation(
        system=BaseSystem(
            list_of_bodies=(
                GravitationalBody(mass=M_sun.value/2, position=Vector(50,200,0), velocity=Vector(0,1.5e-5,0)),
                GravitationalBody(mass=M_sun.value/2, position=Vector(200,350,0), velocity=Vector(1.5e-5,0,0)),
                GravitationalBody(mass=M_sun.value/2, position=Vector(350,200,0), velocity=Vector(0,-1.5e-5,0)),
                GravitationalBody(mass=M_sun.value/2, position=Vector(200,50,0), velocity=Vector(-1.5e-5,0,0))
            ),
            n=9
        ),
        maximum_delta_time=1000
    )
    # sim.show_2D(
    #     traces=True,
    #     display_clock=True,
    #     window_size=(400,400),
    #     screen_color=(255,255,255),
    #     clock_font=(("Trebuchet MS", 25), "black")
    # )
    sim.show_3D(
        show_potential=True,
        # model_size_type="realistic",
        model_size_type="exaggerated",
        window_size=(1440,900),
        camera_movement_mode="instantaneous"
        # camera_movement_mode="cinematic"
    )
