from src.engines.engine_2D.engine import Engine_2D
from src.systems.base_system import BaseSystem
from src.bodies.gravitational_body import GravitationalBody
from src.tools.vector import Vector
from src.simulator.simulation import Simulation


test_system = BaseSystem(
    list_of_bodies=[
        GravitationalBody(position=Vector(250,250,0), mass=1.989*10**30, fixed=True),
        GravitationalBody(position=Vector(100,250,0), mass=5.972*10**24,
                          velocity=Vector(0,-29.78e-6,0), has_potential=False),
        GravitationalBody(position=Vector(400,250,0), mass=5.972*10**24,
                          velocity=Vector(0,29.78e-6,0), has_potential=False),
    ],
    n=9
)
# test_system.show(show_potential=True)

sim = Simulation(
    system=test_system,
    maximum_delta_time=100
)

sim.show(
    window_size=(500,500),
    framerate=60,
    fullscreen=False,
    screen_color=(0,60,60),
    traces=[False, True, True]
)
