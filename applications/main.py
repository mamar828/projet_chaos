from src.engines.engine_2D.engine import Engine_2D
from src.systems.base_system import BaseSystem
from src.bodies.gravitational_body import GravitationalBody
from src.tools.vector import Vector

# listi = [
#     {"object_instance": Flat_earth(position=(51,51)), "model": Rectangle, "color": "blue", "scale": (100,100)},
#     {"object_instance": Flat_earth(position=(849,51)), "model": Circle, "color": "yellow", "scale": (100,100)},
#     {"object_instance": t(position=(700,600)), "model": Circle, "color": "orange", "scale": (80,150)}
# ]

test_system = BaseSystem(
    list_of_bodies=[
        GravitationalBody(position=Vector(250,250,0), mass=2*10**30, fixed=True),
        GravitationalBody(position=Vector(100,250,0), mass=6*10**24),
    ],
    n=9
)
# test_system.show(show_potential=True)

app = Engine_2D(
    window_size=(500,500),
    framerate=5,
    fullscreen=False,
    screen_color=(0,60,60),
    system=test_system
)
app.run()
