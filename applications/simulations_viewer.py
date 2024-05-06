from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import numpy as np
from copy import deepcopy
from eztcolors import Colors as C

from src.simulator.simulation import Simulation
from src.systems.base_system import BaseSystem
from src.systems.computed_system import ComputedSystem
from src.bodies.gravitational_body import GravitationalBody
from src.engines.engine_3D.elements import Function3D, Object3D
from src.engines.engine_3D.models import Cube
from src.tools.vector import Vector
from applications.simulations_examples import sun, earth



if __name__ == '__main__':
    sim = Simulation.load_from_folder(f"simulations/single_body_2d_1")
    # sim.show_3D(
    #     show_potential=True,
    #     # model_size_type="realistic",
    #     model_size_type="exaggerated",
    #     window_size=(1920,1080)
    #     # window_size=(1440,900)
    # )
    sim.show_2D(
        window_size=(900,900),
        fullscreen=False,
        screen_color=(0,60,60),
        display_clock=True,
        traces=True
    )
