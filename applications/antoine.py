from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import numpy as np
from astropy.constants import M_sun

from src.systems.base_system import BaseSystem
from src.bodies.gravitational_body import GravitationalBody
from src.bodies.fake_body import *
from src.tools.vector import Vector
from src.simulator.simulation_mother import SimulationMother
from src.simulator.simulation import Simulation
from src.simulator.lambda_func import Lambda
from applications.simulations_examples import sun, earth, moon
from src.engines.engine_3D.elements import *
from src.engines.engine_3D.models import *
from src.engines.engine_3D.engine import Engine3D
from src.engines.engine_2D.engine import Engine2D
from src.engines.engine_2D.object_2D import Object2D
from src.engines.engine_2D.models import *


# One example at a time to reset the bodies' positions

def all_lagrange_points():
    sim = Simulation(system=BaseSystem([sun, earth, L1Body(), L2Body(), L3Body(), L4Body(), L5Body()]))
    sim.show_3D(
        show_potential=True,
        # model_size_type="realistic",
        model_size_type="exaggerated",
        # window_size=(1920,1080)
        window_size=(1440,900)
    )


all_lagrange_points()


def earth_amplified():
    sim = Simulation(system=BaseSystem([sun, 
        GravitationalBody(mass=earth.mass*50000, position=Vector(400,450,0), velocity=earth.velocity)]))
    sim.show_3D(
        show_potential=True,
        # model_size_type="realistic",
        model_size_type="exaggerated",
        window_size=(1920,1080)
        # window_size=(1440,900)
    )


# earth_amplified()


def sun_earth_moon():
    sim = Simulation(system=BaseSystem([sun, earth, moon]))
    sim.show_3D(
        show_potential=True,
        model_size_type="realistic",
        # model_size_type="exaggerated",
        window_size=(1920,1080),
        # window_size=(1440,900),
        model_saturation=False
    )


# sun_earth_moon()


def plot_your_func():
    Engine3D(
        window_size=(1920,1080),
        functions=[
            Function3D(texture=0, x_limits=(-500,500), y_limits=(-500,500), resolution=200,
                       function=lambda x, y: 20 * np.sin(0.1*x) * np.sin(0.1*y))
        ],
        simulation_presets_allowed=False,
        model_saturation=False,
        light_position=(50,50,50),
        light_color=(5,5,5),
    ).run()


# plot_your_func()


def chaos_example():
    circular_bodies = []
    N=7
    for i in range(N):
        circular_bodies.append(GravitationalBody(
            mass=M_sun.value,
            position=Vector(450+150*np.cos(2*i*np.pi/N), 450+150*np.sin(2*i*np.pi/N), 0),
            velocity=Vector(-5*np.sin(2*i*np.pi/N)*0.5002*10**-5, 5*np.cos(2*i*np.pi/N)*0.5002*10**-5, 0)
        ))

    sim_system = BaseSystem(list_of_bodies=circular_bodies, n=9, method="force")

    sim = Simulation(system=sim_system, maximum_delta_time=1000)
    sim.show_2D(traces=True, display_clock=True)


# chaos_example()
