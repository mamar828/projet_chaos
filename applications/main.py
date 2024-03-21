from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

from datetime import datetime

from src.systems.base_system import BaseSystem
from src.bodies.gravitational_body import GravitationalBody
from src.tools.vector import Vector
from src.simulator.simulation import Simulation
from src.simulator.simulation_mother import Simulation_mother


# test_system = BaseSystem(
#     list_of_bodies=[
#         GravitationalBody(position=Vector(250,250,1), mass=1.989*10**30, fixed=True),
#         GravitationalBody(position=Vector(100,250,1), mass=5.972*10**24,
#                           velocity=Vector(0,-29.78e-6,0), has_potential=False)
#     ],
#     n=9
# )

# sim = Simulation(
#     system=test_system,
#     maximum_delta_time=100
# )

# sim.show(
#     window_size=(500,500),
#     framerate=30,
#     fullscreen=False,
#     screen_color=(0,60,60),
#     traces=[False, True],
#     display_clock=True
# )



if __name__ == '__main__':
    # sim_system = BaseSystem(
    #     list_of_bodies=[GravitationalBody(position=Vector(250,250,0), mass=1.989e30, fixed=True)],
    #     n=9
    # )

    # mommy = Simulation_mother(base_system=sim_system, delta_time=100)
    # foldername = mommy.dispatch(
    #     simulation_count=8,
    #     bodies_per_simulation=3,
    #     body_position_limits=[(200, 300), (200, 300), (0, 0)],
    #     body_velocity_limits=[(-50e-6, 50e-6), (-50e-6, 50e-6), (0, 0)],
    #     save_foldername=f"simulations/test_1",
    #     simulation_duration=10e7,
    #     positions_saving_frequency=1e2
    # )

    # input()

    # sim_viewer = Simulation.load_from_folder(foldername)
    sim_viewer = Simulation.load_from_folder(f"simulations/test_57")
    # sim_viewer = Simulation.load_from_folder(f"simulations/test_53")
    sim_viewer.show(
        window_size=(500,500),
        framerate=60,
        fullscreen=False,
        screen_color=(0,60,60),
        display_clock=True
    )

    # CREATE A BaseSystem FROM THE RESULTS OF THE SIMULATION
    # body = sim_viewer.system.list_of_bodies[3]
    # gbody = GravitationalBody(
    #     mass=body.mass,
    #     position=body.position,
    #     velocity=body.velocity
    # )

    # test_sim = Simulation(
    #     BaseSystem(list_of_bodies=[sim_viewer.system.list_of_bodies[0], gbody], n=9)
    # )
    # test_sim.show(
    #     window_size=(500,500),
    #     framerate=60,
    #     fullscreen=False,
    #     screen_color=(0,60,60),
    #     display_clock=True
    # )
    
    pass
