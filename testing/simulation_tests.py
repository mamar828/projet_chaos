import matplotlib.pyplot as plt
import numpy as np
import timeit

from src.fields.scalar_field import ScalarField
from src.bodies.gravitational_body import GravitationalBody
from src.tools.vector import Vector
from src.systems.base_system import BaseSystem


# body_1 = GravitationalBody(5.97219*10**24, Vector(0, 0, 0), Vector(0, 0, 0), fixed=True)
# body_2 = GravitationalBody(1*10**24, Vector(0, 0, -6.371*10**6),  Vector(0, 0, 0), has_potential=False)
#
# sys = BaseSystem([body_1, body_2], n=0)
# position = []
# velocity = []
# for i in range(8500):
#     sys.update(0.1)
#     # body_2(1, body_1.potential)
#     # print(body_2.velocity)
#     position.append(body_2.position.z)
#     velocity.append(body_2.velocity.z)
# plt.plot(position)
# # plt.plot(velocity)
# plt.show()

sim_system = BaseSystem(
        list_of_bodies=[GravitationalBody(position=Vector(450,450,0), mass=1.989e30, fixed=True),
                        GravitationalBody(position=Vector(300,450,0), velocity=Vector(0,30e-6,0), mass=5.972e29, fixed=False)],
        n=9
    )
sim_system.show(show_bodies=True, show_potential=True, axes={"x": 900, "y": 900})

# setup = """ from time import time"""
# print(timeit.timeit("start = time.time(); trash = time.time();end = time.time(); print(end-start)", number=10000)/10000)
