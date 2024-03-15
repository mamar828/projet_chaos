import matplotlib.pyplot as plt
import numpy as np

from src.fields.scalar_field import ScalarField
from src.bodies.gravitational_body import GravitationalBody
from src.tools.vector import Vector
from src.systems.base_system import BaseSystem


body_1 = GravitationalBody(50, Vector(0.5, -1, 0), Vector(0, 0, 0))
body_2 = GravitationalBody(50, Vector(-1, -1, 0),  Vector(0, 0, 0))
body_3 = GravitationalBody(50, Vector(0, 0, 0), Vector(0, 0, 0))
# body_4 = GravitationalBody(1, Vector(1, 1, 0), Vector(0, 0, 0))
# field = body_1.potential + body_2.potential + body_3.potential

sys = BaseSystem([body_1, body_2, body_3])
sys.show(['b', 'r', 'm'], show_potential=False)

# body_1(1, body_1.potential)
# print(body_1.position)
# body_1(1, body_1.potential)
# print(body_1.position)
# body_1(1, body_1.potential)
# print(body_1.position)
# body_1(1, body_1.potential)
# print(body_1.position)
# body_1(0.1, field-body_1.potential)
# print(body_1.position)
# body_1(0.1, field-body_1.potential)
# print(body_1.position)
# body_1(0.1, field-body_1.potential)
# print(body_1.position)
# body_1(0.1, field-body_1.potential)
# print(body_1.position)

