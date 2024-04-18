from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

from astropy.constants import M_sun

from src.systems.base_system import BaseSystem
from src.systems.new_system import NewSystem
from src.bodies.gravitational_body import GravitationalBody
from src.bodies.fake_body import FakeBody
from src.bodies.new_body import NewBody
from src.tools.vector import Vector
from src.simulator.simulation_mother import SimulationMother
from src.simulator.simulation import Simulation
from src.simulator.lambda_func import Lambda
from applications.simulations_examples import sun, earth



if __name__ == '__main__':
    sim_system = BaseSystem(list_of_bodies=[sun, earth, FakeBody(type="L1")], n=9)
    bb = Simulation.load_from_folder("simulations/L1_tracking_3", only_load_best_body=True).system.get_best_body()

    mommy = SimulationMother(base_system=sim_system)
    foldername = mommy.dispatch(
        simulation_count=500,
        bodies_per_simulation=100,
        delta_time=200,
        body_initial_position_limits=[(bb.initial_position.x*0.99999, bb.initial_position.x*1.00001),
                                      (bb.initial_position.y*0.99999, bb.initial_position.y*1.00001), (0, 0)],
        body_initial_velocity_limits=[(0,                              0),
                                      (bb.initial_velocity.y*0.99999, bb.initial_velocity.y*1.00001), (0, 0)],
        # body_initial_position_limits=[(earth.position.x+1.5-0.1, earth.position.x+1.5+0.1),
        #                               (earth.position.y-0.1,     earth.position.y+0.1), (0, 0)],
        # body_initial_velocity_limits=[(earth.velocity.x-4e-7,    earth.velocity.x+4e-7),
        #                               (earth.velocity.y-4e-7,    earth.velocity.y+4e-7), (0, 0)],
        # body_initial_position_limits=[(sim_system.fake_body.position.x-0.001, sim_system.fake_body.position.x+0.001),
        #                               (sim_system.fake_body.position.y-0.001, sim_system.fake_body.position.y+0.001), 
        #                               (0,                                     0)],
        # body_initial_velocity_limits=[(0,                                     0),
        #                               (earth.velocity.y+2e-7,                 earth.velocity.y+3e-7),
        #                               (0,                                     0)],
        # body_initial_position_limits=[(earth.position.x+1.5, earth.position.x+1.5),
        #                               (earth.position.y,     earth.position.y), (0, 0)],
        # body_initial_velocity_limits=[(earth.velocity.x,    earth.velocity.x),
        #                               (earth.velocity.y+1e-7,    earth.velocity.y+1e-7), (0, 0)],
        save_foldername=f"simulations/L1_tracking",
        simulation_duration=4e7,
        integrator="synchronous",
        positions_saving_frequency=250,
        potential_gradient_limit=1e-10,
        body_alive_func=Lambda("lambda x, y, z, t_x, t_y, t_z: " + 
                        "-0.03 < x - t_x < 0.03 and -0.03 < y - t_y < 0.03", 6)
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
