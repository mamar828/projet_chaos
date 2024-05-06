from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

from astropy.constants import M_sun

from src.systems.base_system import BaseSystem
from src.systems.new_system import NewSystem
from src.bodies.gravitational_body import GravitationalBody
from src.bodies.fake_body import *
from src.bodies.new_body import NewBody
from src.tools.vector import Vector
from src.simulator.simulation_mother import SimulationMother
from src.simulator.simulation import Simulation
from src.simulator.lambda_func import Lambda
from applications.simulations_examples import sun, earth



if __name__ == '__main__':
    sim_system = BaseSystem(list_of_bodies=[sun], n=9)
    # bb = Simulation.load_from_folder("simulations/L2", only_load_best_body=True).system.get_best_body()

    mommy = SimulationMother(base_system=sim_system)
    foldername = mommy.dispatch(
        simulation_count=50,
        bodies_per_simulation=10,
        delta_time=5000,
        # body_initial_position_limits=[(bb.initial_position.x*0.999999, bb.initial_position.x*1.000001),
        #                               (bb.initial_position.y*0.999999, bb.initial_position.y*1.000001), (0, 0)],
        # body_initial_velocity_limits=[(0,                              0),
        #                               (bb.initial_velocity.y*0.999999, bb.initial_velocity.y*1.000001), (0, 0)],
        # body_initial_position_limits=[(earth.position.x+1.5-0.1, earth.position.x+1.5+0.1),
        #                               (earth.position.y-0.1,     earth.position.y+0.1), (0, 0)],
        # body_initial_velocity_limits=[(earth.velocity.x-4e-7,    earth.velocity.x+4e-7),
        #                               (earth.velocity.y-4e-7,    earth.velocity.y+4e-7), (0, 0)],
        # body_initial_position_limits=[
        #     (sim_system.fake_bodies[0].position.x-10, sim_system.fake_bodies[0].position.x+10),
        #     (sim_system.fake_bodies[0].position.y-10, sim_system.fake_bodies[0].position.y+10), 
        #     (0,                                          0)
        # ],
        # body_initial_velocity_limits=[
        #     (earth.velocity.x-200e-7,                  earth.velocity.x-300e-7),
        #     (earth.velocity.y+110e-7,                   earth.velocity.y+170e-7),
        #     (0,                                        0)
        # ],
        # body_initial_position_limits=[(363.95, 383.95), (308.2775360844, 328.2775360844), (0, 0)],
        # body_initial_velocity_limits=[(2e-05, 3e-05), (-1.829e-05, -1.229e-05), (0, 0)],
        # body_initial_position_limits=[(earth.position.x+1.5, earth.position.x+1.5),
        #                               (earth.position.y,     earth.position.y), (0, 0)],
        # body_initial_velocity_limits=[(earth.velocity.x,    earth.velocity.x),
        #                               (earth.velocity.y+1e-7,    earth.velocity.y+1e-7), (0, 0)],
        body_initial_position_limits=[(sun.position.x-200, sun.position.x+200),
                                      (sun.position.y-200, sun.position.y+200),
                                      (0,0)],
        body_initial_velocity_limits=[(-1e-4, 1e-4),
                                      (-1e-4, 1e-4),
                                      (0,0)],
        save_foldername=f"simulations/single_body_2d",
        simulation_duration=3e8,
        integrator="synchronous",
        positions_saving_frequency=1,
        potential_gradient_limit=1e-10,
        # body_alive_func=Lambda("lambda x, y, z, t_x, t_y, t_z: " + 
        #                 "-15 < x - t_x < 15 and -15 < y - t_y < 15", 6)
    )



# if __name__ == '__main__':
#     sun = NewBody(mass=M_sun.value, position=Vector(0,0,0), fixed=True, integrator="synchronous")
#     sim_system = BaseSystem(list_of_bodies=[sun], n=9)
#     # bb = Simulation.load_from_folder("simulations/L1_2").system.get_best_body()

#     mommy = SimulationMother(base_system=sim_system)
#     foldername = mommy.dispatch(
#         simulation_count=500,
#         bodies_per_simulation=25,
#         delta_time=5000,
#         body_initial_position_limits=[(-100,100),
#                                       (-100,100),
#                                       (-100,100)],
#         body_initial_velocity_limits=[(-1e-4,1e-4),
#                                       (-1e-4,1e-4),
#                                       (-1e-4,1e-4)],
#         save_foldername=f"simulations/cool",
#         simulation_duration=1e8,
#         integrator="synchronous",
#         positions_saving_frequency=1,
#         potential_gradient_limit=1e-10,
#         body_alive_func=Lambda("lambda x, y, z: -250 < x < 250 and -250 < y < 250 and -250 < z < 250", 3)
#     )
