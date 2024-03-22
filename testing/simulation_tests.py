import matplotlib.pyplot as plt
import numpy as np

from src.fields.scalar_field import ScalarField
from src.bodies.gravitational_body import GravitationalBody
from src.tools.vector import Vector
from src.systems.base_system import BaseSystem


body_1 = GravitationalBody(5.97219*10**24, Vector(0, 0, 0), Vector(0, 0, 0), fixed=True)
body_2 = GravitationalBody(1*10**24, Vector(0, 0, -6.371*10**6),  Vector(0, 0, 0), has_potential=False)
# body_3 = GravitationalBody(50, Vector(0, 0, 0), Vector(0, 0, 0))
# body_4 = GravitationalBody(1, Vector(1, 1, 0), Vector(0, 0, 0))
# field = body_1.potential + body_2.potential + body_3.potential

# sys = BaseSystem([body_1, body_2, body_3])
# sys.show(['b', 'r', 'm'], show_potential=False)
sys = BaseSystem([body_1, body_2], n=0)
# sys.show(show_potential=True)
# plt.imshow(body_1.potential.get_potential_field(Vector(-6.371*10**6, -6.371*10**6, -6.371*10**6), Vector(6.371*10**6, 6.371*10**6, 6.371*10**6), {"x":200, "y":200}, (0, 0, 0)))
# plt.show()
position = []
velocity = []
for i in range(850):
    sys.update(1)
    # body_2(1, body_1.potential)
    # print(body_2.velocity)
    position.append(body_2.position.z)
    velocity.append(body_2.velocity.z)
# plt.plot(position)
plt.plot(velocity)
plt.show()
# print("position", body_2.position)
# print("velocity", body_2.velocity)
# # print(body_1.potential.get_gradient(body_2.position))
# body_2(100, body_1.potential)
# print("position", body_2.position)
# print("velocity", body_2.velocity)
# # print(body_1.potential.get_gradient(body_2.position))
# body_2(100, body_1.potential)
# print("position", body_2.position)
# print("velocity", body_2.velocity)
# # print(body_1.potential.get_gradient(body_2.position))
# body_2(100, body_1.potential)
# print("position", body_2.position)
# print("velocity", body_2.velocity)
# # print(*body_1.potential.get_gradient(body_2.position))
# body_2(100, body_1.potential)
# print("position", body_2.position)
# print("velocity", body_2.velocity)
# # print(body_1.potential.get_gradient(body_2.position))
# # body_1(0.1, field-body_1.potential)
# # print(body_1.position)
# # body_1(0.1, field-body_1.potential)
# # print(body_1.position)
# # body_1(0.1, field-body_1.potential)
# # print(body_1.position)
# # body_1(0.1, field-body_1.potential)
# # print(body_1.position)
#
