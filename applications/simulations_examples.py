from src.systems.base_system import BaseSystem
from src.bodies.gravitational_body import GravitationalBody
from src.tools.vector import Vector



earth_sun_system = BaseSystem(
        list_of_bodies=[GravitationalBody(position=Vector(450,450,0), mass=1.989e30, fixed=True),
                        GravitationalBody(position=Vector(300,450,0),
                                          velocity=Vector(0,30e-6,0), mass=5.972e24, fixed=False)],
        n=9
    )

interesting_system = BaseSystem(
        list_of_bodies=[GravitationalBody(position=Vector(450,450,0), mass=1.989e30, fixed=False, integrator="kick-drift-kick"),
                        GravitationalBody(position=Vector(300,450,0),
                                          velocity=Vector(0,30e-6,0), mass=5.972e29, fixed=False, integrator="kick-drift-kick")],
        n=9
    )       # Play with the second mass

funny_yeeting = BaseSystem(list_of_bodies=[
    GravitationalBody(mass=1e30, position=Vector(250,250,0), integrator="kick-drift-kick"),
    GravitationalBody(mass=3e30, position=Vector(450,450,0), integrator="kick-drift-kick"),
    GravitationalBody(mass=1e30, position=Vector(650,650,0), integrator="kick-drift-kick")
])
