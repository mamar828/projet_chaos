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
        GravitationalBody(position=Vector(200,350,0), mass=1),
        GravitationalBody(position=Vector(200,200,0), mass=10, fixed=True),
    ]
)

app = Engine_2D(
    window_size=(400,400),
    framerate=1,
    fullscreen=False,
    screen_color=(0,60,60),
    system=test_system
)
app.run()
