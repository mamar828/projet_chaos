from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

from src.systems.base_system import BaseSystem
from src.systems.new_system import NewSystem
from src.bodies.gravitational_body import GravitationalBody
from src.tools.vector import Vector
from src.simulator.simulation_mother import SimulationMother
from src.simulator.simulation import Simulation
from src.simulator.lambda_func import Lambda
from applications.simulations_examples import sun, earth



if __name__ == '__main__':
    sim_system = NewSystem(list_of_bodies=[sun, earth], n=9)
    # bb = Simulation.load_from_folder("simulations/L1_2").system.get_best_body()

    mommy = SimulationMother(base_system=sim_system)
    foldername = mommy.dispatch(
        simulation_count=1,
        bodies_per_simulation=1,
        delta_time=1000,
        # body_initial_position_limits=[(bb.initial_position.x*0.9999, bb.initial_position.x*1.0001),
        #                               (bb.initial_position.y*0.9999, bb.initial_position.y*1.0001), (0, 0)],
        # body_initial_velocity_limits=[(bb.initial_velocity.x*0.9999, bb.initial_velocity.x*1.0001),
        #                               (bb.initial_velocity.y*0.9999, bb.initial_velocity.y*1.0001), (0, 0)],
        # body_initial_position_limits=[(earth.position.x+1.5-0.2, earth.position.x+1.5+0.2),
        #                               (earth.position.y-0.1,     earth.position.y+0.1), (0, 0)],
        # body_initial_velocity_limits=[(earth.velocity.x-1e-7,    earth.velocity.x+1e-7),
        #                               (earth.velocity.y-3e-7,    earth.velocity.y+3e-7), (0, 0)],
        body_initial_position_limits=[(earth.position.x+1.5, earth.position.x+1.5),
                                      (earth.position.y,     earth.position.y), (0, 0)],
        body_initial_velocity_limits=[(earth.velocity.x,    earth.velocity.x),
                                      (earth.velocity.y+1e-7,    earth.velocity.y+1e-7), (0, 0)],
        save_foldername=f"simulations/new_methods",
        simulation_duration=3e7,
        integrator="synchronous",
        positions_saving_frequency=1,
        potential_gradient_limit=5000
        # potential_gradient_limit=1e-10,
        # body_alive_func=Lambda("lambda x, y, z, t_x, t_y, t_z: (1.2 < ((x-t_x)**2 + (y-t_y)**2)**0.5 < 1.8)", 6)
    )


# if __name__ == '__main__':
    # sim_system = BaseSystem(list_of_bodies=[sun], n=9)
    # # bb = Simulation.load_from_folder("simulations/L1_2").system.get_best_body()

    # mommy = SimulationMother(base_system=sim_system)
    # foldername = mommy.dispatch(
    #     simulation_count=32,
    #     bodies_per_simulation=40,
    #     delta_time=5000,
    #     body_initial_position_limits=[(400,500),
    #                                   (400,500),
    #                                   (-50,50)],
    #     body_initial_velocity_limits=[(-1e-4,1e-4),
    #                                   (-1e-4,1e-4),
    #                                   (-1e-4,1e-4)],
    #     save_foldername=f"simulations/test_cool",
    #     simulation_duration=1e8,
    #     integrator="synchronous",
    #     positions_saving_frequency=1,
    #     potential_gradient_limit=1e-9,
    #     # body_alive_func=Lambda("lambda x, y, z, t_x, t_y, t_z: (1.2 < ((x-t_x)**2 + (y-t_y)**2)**0.5 < 1.8)", 6)
    # )
