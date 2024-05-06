from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import numpy as np
import matplotlib.pyplot as plt
import pyregion
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
from src.engines.engine_3D.elements import Function3D

from astropy.constants import M_sun
from astropy.io import fits
# sun2 = GravitationalBody(mass=M_sun.value, position=Vector(450,440,0), fixed=True, integrator="synchronous")


# plot_system = BaseSystem(list_of_bodies=[sun, earth], n=9)
# potential = np.squeeze(plot_system.get_potential_function().get_potential_field(Vector(0, 0, 0), Vector(900, 300, 0), {"x": 1500, "y": 1500}, origin_position=(0, 0, 0)))
# # region = pyregion.open("/Users/felixdesroches/Desktop/Stages_notes/code_chaos/projet_chaos/circ.reg")
# # mask = region.get_mask(fits.PrimaryHDU(potential))
# # mask = np.where(mask == True, np.nan, 1)
# # masked_potential = potential*mask
# plt.imshow(potential, cmap="binary")
# plt.contour(potential, 50, corner_mask=True)
# plt.show()

# if __name__ == '__main__':
#     # toy_system = BaseSystem(list_of_bodies=[sun, earth, L2Body()], n=9)
#     # a = GravitationalBody(
#     #     mass=1,
#     #     position=(toy_system.list_of_bodies[-1].position + Vector(0,0.001,0)),
#     #     velocity=(toy_system.list_of_bodies[-2].velocity - Vector(0,2.9e-7,0)),
#     #     has_potential=False
#     # )
#     # b = GravitationalBody(
#     #     mass=1,
#     #     position=(toy_system.list_of_bodies[-1].position - Vector(0,0.001,0)),
#     #     velocity=(toy_system.list_of_bodies[-2].velocity - Vector(0,3.1e-7,0)),
#     #     has_potential=False
#     # )
sim_system = BaseSystem(list_of_bodies=[sun, earth, L1Body(), L2Body(), L3Body(), L4Body(), L5Body()], n=9)
#     # sim_system = BaseSystem(list_of_bodies=[sun, earth, L1Body(), L2Body(), L3Body(), L4Body(), L5Body()], n=9)
#     # bb = Simulation.load_from_folder("simulations/L1_2").system.get_best_body()
#
sim = Simulation(system=sim_system, maximum_delta_time=10000)
sim.run(
    duration=1e8,
    positions_saving_frequency=10,
    potential_gradient_limit=None,
    body_alive_func=None
)
sim.show_2D(traces=False, display_clock=True, window_size=(900,900), screen_color=(27, 33, 44))
#     sim.show_3D(
#         show_potential=True,
#         # model_size_type="realistic",
#         model_size_type="exaggerated",
#         window_size=(1440,900),
#         camera_movement_mode="instantaneous"
#         # camera_movement_mode="cinematic"
#     )
