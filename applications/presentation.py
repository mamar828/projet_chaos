from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import numpy as np
from astropy.constants import M_sun

from src.systems.base_system import BaseSystem
from src.systems.new_system import NewSystem
from src.bodies.gravitational_body import GravitationalBody
from src.bodies.fake_body import *
from src.bodies.new_body import NewBody
from src.tools.vector import Vector
from src.simulator.simulation_mother import SimulationMother
from src.simulator.simulation import Simulation
from src.simulator.lambda_func import Lambda
from applications.simulations_examples import sun, earth, moon
from src.engines.engine_3D.elements import *
from src.engines.engine_3D.models import *
from src.engines.engine_3D.engine import Engine3D
from src.engines.engine_2D.engine import Engine2D
from src.engines.engine_2D.object_2D import Object2D
from src.engines.engine_2D.models import *


def meme_bremss():
    # sim_system = BaseSystem(list_of_bodies=[sun, earth, L1Body(), L2Body(), L3Body(), L4Body(), L5Body()], n=9)
    sim = Simulation(
        system=BaseSystem(
            list_of_bodies=(
                sun,
                earth
            ),
            n=9
        ),
        maximum_delta_time=1000
    )
    # sim.show_2D(
    #     traces=True,
    #     display_clock=True,
    #     window_size=(400,400),
    #     screen_color=(255,255,255),
    #     clock_font=(("Trebuchet MS", 25), "black")
    # )
    sim.show_3D(
        show_potential=True,
        functions=[
            Function3D(texture="bremss_1", instance=sim.system, x_limits=(0,900), y_limits=(0,900),
                        resolution=200, hidden=True),
            Function3D(texture="bremss_2", instance=sim.system, x_limits=(0,900), y_limits=(0,900),
                        resolution=200, hidden=True, rotation=(0,0,90), position=(900,0,0))
        ],
        objects=[Object3D()],
        # fullscreen=False,
        # model_size_type="realistic",
        model_size_type="exaggerated",
        # window_size=(1000,600),
        window_size=(1440,900),
        # window_size=(1920,1080),
        # camera_cinematic_settings=cinematic_movement
    )


# meme_bremss()


def dvd():
    class DVD:
        def __init__(self, position, color):
            self.x_position, self.y_position = position
            self.x_direction = 1
            self.y_direction = 1
            self.x_limits = [50,697-50]
            self.y_limits = [50,523-50]
            self.color = color

        def update(self, delta_time):
            if self.x_position > self.x_limits[1]:
                self.x_direction *= -1
                self.change_color()
            if self.x_position < self.x_limits[0]:
                self.x_direction *= -1
                self.change_color()
            if self.y_position < self.y_limits[0]:
                self.y_direction *= -1
                self.change_color()
            if self.y_position > self.y_limits[1]:
                self.y_direction *= -1
                self.change_color()
            self.x_position += 200 * delta_time * self.x_direction
            self.y_position += 200 * delta_time * self.y_direction

        @property
        def position(self):
            return self.x_position, self.y_position

        def change_color(self):
            self.color = np.random.randint(0, 255, 3)


    Engine2D(
        objects=[Object2D(color="yellow", position=(500,500), scale=(100,100), model=Rectangle,
                          instance=DVD((350,50), "green"))],
        window_size=(697,523),
        screen_color=(0,0,0)
    ).run()


# dvd()


def L1_viewer_single():
    sim = Simulation.load_from_folder(f"simulations/L1_tracking_5", only_load_best_body=True)
    input("loaded")
    sim.show_3D(
        show_potential=True,
        model_size_type="realistic",
        functions=[
            Function3D(texture="bremss_1", instance=sim.system, x_limits=(0,900), y_limits=(0,900),
                        resolution=200, hidden=True)
            # Function3D(texture="bremss_2", instance=sim.system, x_limits=(0,900), y_limits=(0,900),
            #             resolution=200, hidden=True, rotation=(0,0,90), position=(900,0,0))
        ],
        # model_size_type="exaggerated",
        window_size=(1920,1080)
        # window_size=(1440,900)
    )


# L1_viewer_single()


def L1_viewer_multiple():
    sim = Simulation.load_from_folder(f"simulations/L1_tracking_5", min_time_survived=1e7)
    input("loaded")
    sim.show_3D(
        show_potential=True,
        model_size_type="realistic",
        functions=[
            Function3D(texture="bremss_1", instance=sim.system, x_limits=(0,900), y_limits=(0,900),
                        resolution=200, hidden=True),
            Function3D(texture="bremss_2", instance=sim.system, x_limits=(0,900), y_limits=(0,900),
                        resolution=200, hidden=True, rotation=(0,0,90), position=(900,0,0))
        ],
        # model_size_type="exaggerated",
        window_size=(1920,1080)
        # window_size=(1440,900)
    )


# L1_viewer_multiple()


def L5_viewer():
    sim = Simulation.load_from_folder(f"simulations/L5", min_time_survived=1e8)
    input("loaded")
    sim.show_3D(
        show_potential=True,
        # model_size_type="realistic",
        model_size_type="exaggerated",
        window_size=(1920,1080)
        # window_size=(1440,900)
    )
 

# L5_viewer()

def presentation():
    sim1 = Simulation.load_from_folder(f"simulations/L1_tracking_5", only_load_best_body=True)
    sim2 = Simulation.load_from_folder(f"simulations/L5", min_time_survived=1e8)
    input("loaded")
    sim1.show_3D(
        show_potential=True,
        model_size_type="realistic",
        functions=[
            # Function3D(texture="bremss_1", instance=sim1.system, x_limits=(0,900), y_limits=(0,900),
            #             resolution=200, hidden=True)
            Function3D(texture="bremss_2", instance=sim1.system, x_limits=(0,900), y_limits=(0,900),
                       resolution=100, hidden=True, rotation=(0,0,90), position=(900,0,0))
        ],
        # model_size_type="exaggerated",
        window_size=(1920,1080)
        # window_size=(1440,900)
    )
    sim2.show_3D(
        show_potential=True,
        # model_size_type="realistic",
        model_size_type="exaggerated",
        window_size=(1920,1080)
        # window_size=(1440,900)
    )


# presentation()


def all_lagrange_points():
    sim = Simulation(system=BaseSystem([sun, earth, L1Body(), L2Body(), L3Body(), L4Body(), L5Body()]))
    sim.show_3D(
        show_potential=True,
        # model_size_type="realistic",
        model_size_type="exaggerated",
        window_size=(1920,1080)
        # window_size=(1440,900)
    )


# all_lagrange_points()


def earth_amplified():
    sim = Simulation(system=BaseSystem([sun, 
        GravitationalBody(mass=earth.mass*50000, position=Vector(400,450,0), velocity=earth.velocity)]))
    sim.show_3D(
        show_potential=True,
        # model_size_type="realistic",
        model_size_type="exaggerated",
        window_size=(1920,1080)
        # window_size=(1440,900)
    )


# earth_amplified()


def sun_earth_moon():
    sim = Simulation(system=BaseSystem([sun, earth, moon]))
    sim.show_3D(
        show_potential=True,
        model_size_type="realistic",
        # model_size_type="exaggerated",
        window_size=(1920,1080),
        # window_size=(1440,900),
        model_saturation=False
    )


# sun_earth_moon()


def size_comparison():
    sim = Simulation(BaseSystem([
        GravitationalBody(mass=sun.mass, position=Vector(0,0,0)),
        GravitationalBody(mass=earth.mass, position=Vector(0,0,0)),
        GravitationalBody(mass=moon.mass, position=Vector(0,0,0)),
        GravitationalBody(mass=moon.mass, position=(moon.position-earth.position))
    ]))
    sim.show_3D(
        model_size_type="realistic",
        window_size=(1920,1080),
        # window_size=(1440,900)
    )


# size_comparison()


def plot_your_func():
    Engine3D(
        window_size=(1920,1080),
        functions=[
            Function3D(texture=2, x_limits=(-100,100), y_limits=(-100,100), resolution=50,
                       function=lambda x, y: np.sin(0.1*x)*np.sin(0.1*y)*30 + 100*np.exp(-(x**2+y**2)/100))
        ],
        simulation_presets_allowed=False,
        model_saturation=False,
        light_position=(50,50,50),
        light_color=(5,5,5),
    ).run()


# plot_your_func()
