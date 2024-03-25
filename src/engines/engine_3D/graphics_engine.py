import pygame as pg
import numpy as np
import moderngl as mgl
import sys
from struct import pack

from model import *
from camera import Camera
from light import Light
from mesh import Mesh
from scene import *
from scene_renderer import Scene_renderer
from tests import Floor, Planet, Mode7
from relative_paths import get_path


class Graphics_engine:
    def __init__(self,
            window_size: tuple[int]=(1440,900),
            framerate: int=60,
            fullscreen: bool=False,
            light_position: tuple[int]=(0,0,0),
            light_color: tuple[int]=(1,1,1),
            light_ambient_intensity: float=0.1,
            light_diffuse_intensity: float=1.5,
            light_specular_intensity: float=1.0,
            camera_origin: tuple[int]=(0,0,0),
            camera_speed: float=0.025,
            camera_sensitivity: float=0.1,
            camera_fov: float=50.,
            camera_near_render_distance: float=0.1,
            camera_far_render_distance: float=100000000000000000000.,
            camera_yaw: float=-90.,
            camera_pitch: float=0.,
            scene_elements: list=None,
            plot_function: bool=False
        ):
        self.window_size = window_size
        self.framerate = framerate
        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)

        pg.display.set_mode(self.window_size, flags=pg.OPENGL | pg.DOUBLEBUF)
        if fullscreen: pg.display.toggle_fullscreen()

        # Mouse settings
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)

        self.context = mgl.create_context()
        self.context.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE)       # Allows for depth testing (z-buffering)
        self.clock = pg.time.Clock()
        self.time = 0
        self.delta_time = 0     # Enables constant camera movement regardless of the framerate

        # self.light = Light(
        #     position=light_position, 
        #     color=light_color,
        #     ambient_intensity=light_ambient_intensity,
        #     diffuse_intensity=light_diffuse_intensity,
        #     specular_intensity=light_specular_intensity
        # )
        # self.camera = Camera(
        #     app=self,
        #     position=camera_origin,
        #     speed=camera_speed,
        #     sensitivity=camera_sensitivity,
        #     fov=camera_fov,
        #     near_render_distance=camera_near_render_distance,
        #     far_render_distance=camera_far_render_distance,
        #     yaw=camera_yaw,
        #     pitch=camera_pitch
        # )
        # self.mesh = Mesh(self)
        # self.scene = Scene(self, scene_elements)#, plot_function=plot_function)
        # self.scene_renderer = Scene_renderer(self)

        with open(get_path("shaders/surface/vertex.glsl")) as f:
            vertex = f.read()
        with open(get_path("shaders/surface/fragment.glsl")) as f:
            fragment = f.read()
        self.program = self.context.program(vertex_shader=vertex, fragment_shader=fragment)
        
        vertices = [(-1,-1),(1,-1),(1,1),(-1,1),(-1,-1),(1,1)]
        vertex_data = pack(f"{len(vertices) * len(vertices[0])}f", *sum(vertices, ()))
        self.vbo = self.context.buffer(vertex_data)
        self.vao = self.context.vertex_array(self.program, [(self.vbo, "2f", "in_position")])
        self.set_uniform("u_resolution", self.window_size)

    def update(self):
        # self.program["camPos"].write(self.camera.position)
        self.set_uniform("u_time", self.time)

    def set_uniform(self, u_name, u_value):
        try:
            self.program[u_name] = u_value
        except KeyError:
            pass

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.scene.destroy()
                pg.quit()
                sys.exit()

    def render(self):
        self.context.clear(color=(0.08, 0.16, 0.18))
        self.vao.render()
        # self.scene_renderer.render()
        pg.display.flip()

    def get_time(self):
        self.time = pg.time.get_ticks() * 0.001

    def run(self):
        while True:
            self.get_time()
            self.check_events()
            # self.camera.update()
            self.update
            self.render()
            self.delta_time = self.clock.tick(self.framerate)


listi = [
    {"object_instance": Planet(position=(2,2,-50)), "model": Sphere, "color": "blue", "scale": (2,1,1)},
    {"object_instance": Floor(position=(0,0,0)), "model": Cube, "color": 3, "scale": (50,1,50)}
]


if __name__ ==  "__main__":
    # Create the graphics engine object
    app = Graphics_engine(
        window_size=(1440,900),
        framerate=60,
        fullscreen=True,
        light_position=(100,30,30),
        light_color=(1,1,1),
        scene_elements=listi,
        plot_function=True
    )
    app.run()
