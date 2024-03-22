from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

from src.simulator.simulation import Simulation



if __name__ == '__main__':
    sim_viewer = Simulation.load_from_folder(f"simulations/dead_method_29")
    sim_viewer.show(
        window_size=(500,500),
        framerate=60,
        fullscreen=False,
        screen_color=(0,60,60),
        display_clock=True,
        traces=True
    )
