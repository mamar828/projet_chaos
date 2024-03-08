import matplotlib.pyplot as plt

from src.fields.scalar_field import ScalarField
from src.bodies.gravitational_body import GravitationalBody
from src.tools.vector import Vector


body_1 = GravitationalBody(10**6, Vector(1, 1, 0), Vector(0, 0, 0))
body_2 = GravitationalBody(10**6, Vector(-1, -1, -0), Vector(0, 0, 0))
body_3 = GravitationalBody(10**6, Vector(0, 0, 0), Vector(0, 0, 0))
# body_4 = GravitationalBody(1, Vector(1, 1, 0), Vector(0, 0, 0))


field = body_1.potential + body_2.potential + body_3.potential
potential_field = field.get_potential_field(Vector(-2, -2, -2), Vector(2, 2, 2), {"x": 666, "y": 666}, (0, 0, 0))
#
# plt.imshow(potential_field, cmap="binary")
# plt.colorbar()
# plt.show()
body_1(0.1, field-body_1.potential)
print(body_1.position)
body_1(0.1, field-body_1.potential)
print(body_1.position)
body_1(0.1, field-body_1.potential)
print(body_1.position)
body_1(0.1, field-body_1.potential)
print(body_1.position)
body_1(0.1, field-body_1.potential)
print(body_1.position)

