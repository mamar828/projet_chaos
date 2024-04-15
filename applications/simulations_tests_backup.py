from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import numpy as np

from src.systems.base_system import BaseSystem
from src.bodies.gravitational_body import GravitationalBody
from src.tools.vector import Vector
from src.simulator.simulation_mother import SimulationMother
from src.simulator.simulation import Simulation
from src.simulator.lambda_func import Lambda
from applications.simulations_examples import sun, earth
from src.engines.engine_3D.elements import Function3D

from astropy.constants import M_sun
sun2 = GravitationalBody(mass=M_sun.value, position=Vector(460,450,0), fixed=True, integrator="synchronous")
circular_bodies = []
N=15
for i in range(N):
    circular_bodies.append(GravitationalBody(mass=M_sun.value, position=Vector(450+150*np.cos(2*i*np.pi/N), 450+150*np.sin(2*i*np.pi/N), 0), velocity=Vector(-1*np.sin(2*i*np.pi/N)*0.5002*10**-5, 1*np.cos(2*i*np.pi/N)*0.5002*10**-5, 0)))
test_0 = GravitationalBody(mass=M_sun.value, position=Vector(300, 450, 0), velocity=Vector(0, 2.0002*10**-5, 0))
test_1 = GravitationalBody(mass=M_sun.value, position=Vector(600, 450, 0), velocity=Vector(0, -2.0002*10**-5, 0))
test_2 = GravitationalBody(mass=M_sun.value, position=Vector(450, 300, 0), velocity=Vector(-2.0002*10**-5, 0, 0))
test_3 = GravitationalBody(mass=M_sun.value, position=Vector(450, 600, 0), velocity=Vector(2.0002*10**-5, 0, 0))

if __name__ == '__main__':
    other_body = GravitationalBody(
        mass=10,
        position=Vector(earth.position.x+1.5, earth.position.y, 0),
        velocity=Vector(earth.velocity.x, earth.velocity.y, 0),
        has_potential=False,
        integrator="synchronous"
    )
    # sim_system = BaseSystem(list_of_bodies=[test_0, test_1, test_2, test_3], n=9, method="force")
    sim_system = BaseSystem(list_of_bodies=circular_bodies, n=9, method="force")
    # sim_system = BaseSystem(list_of_bodies=[sun, sun2, earth], n=9, method="force")
    # bb = Simulation.load_from_folder("simulations/L1_2").system.get_best_body()

    sim = Simulation(system=sim_system, maximum_delta_time=1000)
    sim.show_2D(traces=True, display_clock=True)
    sim.show_3D(
        show_potential=True,
        # model_size_type="realistic",
        model_size_type="exaggerated",
        window_size=(1680,1050),
        # camera_position_mode="following",
        camera_position_mode="free",
        camera_movement_mode="instantaneous"
        # camera_movement_mode="cinematic"
    )
