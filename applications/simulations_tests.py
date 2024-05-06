from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import numpy as np

from src.systems.base_system import BaseSystem
from src.bodies.gravitational_body import GravitationalBody
from src.bodies.fake_body import *
from src.tools.vector import Vector
from src.simulator.simulation_mother import SimulationMother
from src.simulator.simulation import Simulation
from src.simulator.lambda_func import Lambda
from applications.simulations_examples import sun, earth
from src.engines.engine_3D.elements import Function3D

from astropy.constants import M_sun

cinematic_movement = {
    "positive_acceleration" : 0.05,
    "negative_acceleration" : 0,
    "positive_rotation" : 0.05,
    "negative_rotation" : 1
}


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
        functions=[
            Function3D("bremss_1", (0,0,100),
            function=lambda x, y: 30 * np.sin(x/20) * np.sin(y/20) + 500 * np.exp(-((x-450)**2+(y-450)**2)/1000), 
            x_limits=(0,900), y_limits=(0,900), resolution=500, hidden=True)],
        # fullscreen=False,
        # model_size_type="realistic",
        model_size_type="exaggerated",
        # window_size=(1000,600),
        window_size=(1440,900),
        # window_size=(1920,1080),
        # camera_cinematic_settings=cinematic_movement
    )
