from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

from src.simulator.simulation import Simulation
from src.systems.computed_system import ComputedSystem



if __name__ == '__main__':
    sim_viewer = Simulation.load_from_folder(f"simulations/double_body_tests")
    # sim_viewer = Simulation(system=ComputedSystem(list_of_bodies=sim_viewer.system.list_of_bodies[:6], n=9,
    #                                               tick_factor=sim_viewer.system.tick_factor))
    sim_viewer.show(
        window_size=(900,900),
        framerate=60,
        fullscreen=False,
        screen_color=(0,60,60),
        display_clock=True,
        traces=True
    )
