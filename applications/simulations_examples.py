import numpy as np
from astropy.constants import M_sun, M_earth

from src.systems.base_system import BaseSystem
from src.bodies.gravitational_body import GravitationalBody
from src.bodies.new_body import NewBody
from src.tools.vector import Vector
from src.engines.engine_3D.elements import *


earth_sun_system = BaseSystem(
        list_of_bodies=[GravitationalBody(position=Vector(450,450,0), mass=1.989e30, fixed=True),
                        GravitationalBody(position=Vector(300,450,0),
                                          velocity=Vector(0,30e-6,0), mass=5.972e24, fixed=False)],
        n=9
    )

interesting_system = BaseSystem(
        list_of_bodies=[GravitationalBody(position=Vector(450,450,0), mass=1.989e30, fixed=False, 
                                          integrator="synchronous"),
                        GravitationalBody(position=Vector(300,450,0), velocity=Vector(0,30e-6,0), mass=5.972e29,
                                          fixed=False, integrator="synchronous")],
        n=9
    )       # Play with the second mass

funny_yeeting = BaseSystem(list_of_bodies=[
    GravitationalBody(mass=1e30, position=Vector(250,250,0)),
    GravitationalBody(mass=3e30, position=Vector(450,450,0)),
    GravitationalBody(mass=1e30, position=Vector(650,650,0))
])

sun = GravitationalBody(mass=M_sun.value, position=Vector(450,450,0), fixed=True, integrator="synchronous")
earth = GravitationalBody(mass=M_earth.value, position=Vector(297.90,450,0),                # Parameters at apoapsis
                            velocity=Vector(0,-29.29e-6,0), fixed=False, integrator="synchronous")
moon = GravitationalBody(mass=7.346e22, position=(earth.position + Vector(405500e-6,0,0)),
                          velocity=(earth.velocity+Vector(0,-0.970e-6,0)))
sim_system = BaseSystem(list_of_bodies=[sun, earth], n=9)

bremss = Function3D(
    "bremss_1", (0,0,100),
    function=lambda x, y: 30 * np.sin(x/20) * np.sin(y/20) + 500 * np.exp(-((x-450)**2+(y-450)**2)/1000), 
    x_limits=(0,900), y_limits=(0,900), resolution=500, hidden=True
)

cinematic_movement = {
    "positive_acceleration" : 0.05,
    "negative_acceleration" : 0,
    "positive_rotation" : 0.05,
    "negative_rotation" : 1
}