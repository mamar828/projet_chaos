from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import numpy as np
from copy import deepcopy

from src.simulator.simulation import Simulation
from src.systems.base_system import BaseSystem
from src.systems.computed_system import ComputedSystem
from src.bodies.gravitational_body import GravitationalBody
from src.engines.engine_3D.elements import Function3D, Object3D
from src.engines.engine_3D.models import Cube
from src.tools.vector import Vector
from applications.simulations_examples import sun, earth



if __name__ == '__main__':
    sim = Simulation.load_from_folder(f"simulations/thrash_8")#, only_load_best_body=True)
    # print(repr(sim.system.list_of_bodies[-1].position))
    # print(repr(sim.system.list_of_bodies[-1].velocity))
    # raise
    # other = sim.system.list_of_bodies[-1].to_gravitational_body()
    # sim.system = ComputedSystem(list_of_bodies=(sim.system.list_of_bodies + [other]), n=9, tick_factor=sim.system.tick_factor)
    # sim.system = sim.system.to_base_system()

    # sim = Simulation(system=BaseSystem(list_of_bodies=[sun, earth, sim.system.list_of_bodies[-1]], n=9))
    # input("loaded")

    sim.show_3D(
        show_potential=True,
        print_camera_coordinates=False,
        model_size_type="realistic",
        window_size=(1440,900),
        camera_position_mode="following",
        camera_movement_mode="instantaneous"
    )
    sim.show_2D(
        window_size=(900,900),
        framerate=60,
        fullscreen=False,
        screen_color=(0,60,60),
        display_clock=True,
        traces=True
    )
