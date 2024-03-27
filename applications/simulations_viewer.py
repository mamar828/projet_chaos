from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import numpy as np

from src.simulator.simulation import Simulation
from src.systems.computed_system import ComputedSystem
from src.engines.engine_3D.elements import Function3D
from src.tools.vector import Vector



if __name__ == '__main__':
    sim = Simulation.load_from_folder(f"simulations/gravity_assist")
    # sim = Simulation(system=ComputedSystem(list_of_bodies=sim.system.list_of_bodies[:6], n=9,
    #                                               tick_factor=sim.system.tick_factor))

    sim.show_3D(
        functions=[Function3D(
            texture="spacetime",
            position=(0,0,0),
            resolution=(200,200),
            x_limits=(0,900),
            y_limits=(0,900),
            # function=lambda x, y: np.exp(-(x**2+y**2)/1000)*2000,
            function=lambda x, y: sim.system.get_potential_function()(Vector(x,y,0)) * 1e10
            # save_filename=("src/engines/engine_3D/vertex_data_cache/test_4.gz")
        )]
    )
    # sim.show_2D(
    #     window_size=(900,900),
    #     framerate=60,
    #     fullscreen=False,
    #     screen_color=(0,60,60),
    #     display_clock=True,
    #     traces=True
    # )
