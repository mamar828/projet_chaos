from src.engines.engine_2D.engine import Engine_2D
from src.systems.base_system import BaseSystem
from src.bodies.gravitational_body import GravitationalBody
from src.tools.vector import Vector
from src.simulator.simulation import Simulation
import numpy as np

from os import environ


environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

theta = 60
test_system = BaseSystem(
    list_of_bodies=[
        GravitationalBody(position=Vector(300,300,0), velocity=Vector(0, 0, 0), mass=1.989*10**30, fixed=True),
        # GravitationalBody(position=Vector(170,245,0), velocity=Vector(0, 21e-6, 0), mass=1.989*10**30, fixed=True),
        # GravitationalBody(position=Vector(245,320,0), velocity=Vector(21e-6, 0, 0), mass=1.989*10**30, fixed=False),
        # GravitationalBody(position=Vector(245,170,0), velocity=Vector(-21e-6, 0, 0), mass=1.989*10**20, fixed=False),
        GravitationalBody(position=Vector(300-150,300,0), mass=5.972*10**24, velocity=Vector(0,-29.78e-6,0), has_potential=True, fixed=False),
        # GravitationalBody(position=Vector(320 - 228, 245, 0), mass=6.39 * 10 ** 24,
        #                   velocity=Vector(0, -24.1308333e-6, 0), has_potential=False),
        GravitationalBody(position=Vector(300-150*np.cos(theta/180*np.pi),300+150*np.sin(theta/180*np.pi),0), mass=5.972*10**24,
                          velocity=Vector(-29.78e-6*np.sin(theta/180*np.pi),-29.78e-6*np.cos(theta/180*np.pi),0), has_potential=False),
        GravitationalBody(
            position=Vector(300 - 150 * np.cos((theta-1) / 180 * np.pi), 300 + 150 * np.sin((theta-1) / 180 * np.pi), 0),
            mass=5.972 * 10 ** 24,
            velocity=Vector(-29.28e-6*np.sin((theta-1)/180*np.pi),-29.28e-6*np.cos((theta-1)/180*np.pi),0), has_potential=False),
        GravitationalBody(
            position=Vector(300 - 150 * np.cos((theta+1) / 180 * np.pi), 300 + 150 * np.sin((theta+1) / 180 * np.pi), 0),
            mass=5.972 * 10 ** 24,
            velocity=Vector(-29.28e-6*np.sin((theta+1)/180*np.pi),-29.28e-6*np.cos((theta+1)/180*np.pi),0), has_potential=False),
        # GravitationalBody(
        #     position=Vector(300 - 150 * np.cos(15 / 180 * np.pi), 300 + 150 * np.sin(15 / 180 * np.pi), 0),
        #     mass=5.972 * 10 ** 24,
        #     velocity=Vector(-29.78e-6 * np.sin(15 / 180 * np.pi), -29.78e-6 * np.cos(15 / 180 * np.pi), 0),
        #     has_potential=False),
    ],
    n=9
)
# test_system.show(show_bodies=True, show_potential_null_slope_points=10**9)

sim = Simulation(
    system=test_system,
    maximum_delta_time=100
)

sim.show(
    window_size=(600,600),
    framerate=60,
    fullscreen=False,
    screen_color=(0,60,60),
    traces=[False, True, False, True, True]
)
