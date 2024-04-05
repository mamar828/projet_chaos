import pygame as pg
import moderngl as mgl

from src.engines.engine_3D.camera import Camera
from src.engines.engine_3D.light import Light
from src.engines.engine_3D.mesh import Mesh
from src.engines.engine_3D.scene import Scene
from src.engines.engine_3D.scene_renderer import SceneRenderer
from src.engines.engine_3D.elements import Object3D, Function3D
from src.engines.global_engine import GlobalEngine


class Engine3D(GlobalEngine):
    def __init__(
            self,
            simulation,#=Simulation                 Cannot provide type due to circular imports
            window_size: tuple[int,int]=(1440,900),
            framerate: int=60,
            fullscreen: bool=True,
            light_position: tuple[int,int,int]=(0,0,0),
            light_color: tuple[int,int,int]=(1,1,1),
            light_ambient_intensity: float=0,
            light_diffuse_intensity: float=1.5,
            light_specular_intensity: float=1.0,
            camera_origin: tuple[int,int,int]=(0,0,0),
            camera_speed: float=0.025,
            camera_sensitivity: float=0.1,
            camera_fov: float=50.,
            camera_near_render_distance: float=0.05,
            camera_far_render_distance: float=1e20,
            camera_yaw: float=-90.,
            camera_pitch: float=0.,
            camera_movement_mode: str="free",
            camera_rotation_mode: str="instantaneous",
            objects: list[Object3D]=None,
            functions: list[Function3D]=None,
            simulation_presets_allowed: bool=True,
            print_camera_coordinates: bool=False,
            model_size_type: str="exaggerated",
        ):
        """ 
        Supported camera_movement_modes are "free" and "following".
        Supported camera_rotation_modes are "instantaneous" and "cinematic".
        Supported model_size_types are "exaggerated" and "realistic".
        """
        # Default parameters for camera origin and light position
        if simulation and simulation_presets_allowed:
            camera_origin = simulation.system.origin
            light_position = simulation.system.origin

        super().__init__(simulation=simulation, window_size=window_size, framerate=framerate, fullscreen=fullscreen)
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
        self.camera_delta_time = 0                                   # Used for constant camera speed regardless of fps
        self.print_camera_coordinates = print_camera_coordinates
        self.model_size_type = model_size_type

        self.light = Light(
            position=light_position, 
            color=light_color,
            ambient_intensity=light_ambient_intensity,
            diffuse_intensity=light_diffuse_intensity,
            specular_intensity=light_specular_intensity
        )
        self.camera = Camera(
            app=self,
            position=camera_origin,
            speed=camera_speed,
            sensitivity=camera_sensitivity,
            fov=camera_fov,
            near_render_distance=camera_near_render_distance,
            far_render_distance=camera_far_render_distance,
            yaw=camera_yaw,
            pitch=camera_pitch,
            movement_mode=camera_movement_mode,
            rotation_mode=camera_rotation_mode
        )
        self.functions = functions
        self.mesh = Mesh(self)
        self.scene = Scene(self, objects)
        self.scene_renderer = SceneRenderer(self)

    def render(self):
        # Update scene and camera before to prevent flickering
        self.scene.update()
        self.camera.update()
        self.context.clear()
        self.scene_renderer.render()
        pg.display.flip()

    def run(self):
        while True:
            self.get_time()
            self.check_events()
            # self.camera.update()
            self.render()
            self.delta_time = (self.clock.tick(self.framerate) / 1000) * self.physics_speed
            self.camera_delta_time = self.clock.tick(self.framerate)
            pg.display.set_caption(f"Current physics speed : x{self.physics_speed:.2e}")
            self.simulation_time += self.delta_time
            if self.print_camera_coordinates:
                print(self.camera)



# elements = [
#     Object3D(instance=Planet(position=(2,2,-50)), model=Sphere, texture="blue", scale=(2,1,1)),
#     Object3D(instance=Floor(position=(0,0,0)), model=Cube, texture=3, scale=(50,1,50))
# ]

# functions = [
#     Function3D(function=lambda x, y: 3000 * np.exp(-(x**2+y**2)/1000) + 10, texture="filix", rotation=(45,0,0)),
#     Function3D(function=lambda x, y: 3000 * np.exp(-(x**2+y**2)/1000) + 10, texture="spacetime", rotation=(-45,0,0)),
#     Function3D(function=lambda x, y: np.sin(x)*np.sin(y) * 2, x_limits=(-100,200), resolution=(1500,1500), texture=0, rotation=(0,0,45), save_filename=get_path("vertex_data_cache/sines2.gz")),
#     Function3D(function=lambda x, y: np.sin(x)*np.sin(y) * 2, x_limits=(-100,200), resolution=(200,200), texture=0, rotation=(0,0,-45))
# ]


# if __name__ ==  "__main__":
#     # Create the graphics engine object
#     app = Engine3D(
#         window_size=(1440,900),
#         framerate=60,
#         fullscreen=True,
#         light_position=(0,30,100),
#         light_color=(1,1,1),
#         scene_elements=elements,
#         functions=functions
#     )
#     app.run()
