import pygame as pg
import moderngl as mgl
from eztcolors import Colors as C

from src.engines.engine_3D.camera import Camera
from src.engines.engine_3D.light import Light
from src.engines.engine_3D.mesh import Mesh
from src.engines.engine_3D.scene import Scene
from src.engines.engine_3D.scene_renderer import SceneRenderer
from src.engines.engine_3D.elements import Object3D, Function3D
from src.engines.global_engine import GlobalEngine
from src.engines.inputs.keyboard import Keyboard

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
            objects: list[Object3D]=None,
            functions: list[Function3D]=None,
            simulation_presets_allowed: bool=True,
            model_size_type: str="exaggerated",
            camera_cinematic_settings: dict={
                "positive_acceleration" : 0.05,
                "negative_acceleration" : 0.05,
                "positive_rotation" : 0.05,
                "negative_rotation" : 0.94
            }
        ):
        """ 
        Supported model_size_types are "exaggerated" and "realistic".
        """
        assert model_size_type in ["exaggerated", "realistic"], (
            f"{C.RED+C.BOLD}model_size_type keyword given is not supported. " +
            f"Supported types are 'exaggerated' and 'realistic', not '{model_size_type}'.{C.END}")

        # Default parameters for camera origin and light position
        if simulation and simulation_presets_allowed:
            camera_origin = simulation.system.origin
            light_position = simulation.system.origin

        self.key_modes = ["presets", "camera", "manual"]
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
            cinematic_settings=camera_cinematic_settings
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

    def get_current_state(self):
        state = {
            "lEngine type" : self.__class__.__name__,
            "Simulation time (s)" : f"{self.simulation_time:.2e}",
            "lWindow size" : self.window_size,
            "Physics speed" : f"{self.physics_speed:.2e}",
            "lFramerate" : self.framerate,
            "Camera pos (x,y,z)" : \
                f"{self.camera.position.x:.3f}, {-self.camera.position.z:.3f}, {self.camera.position.y:.3f}",
            "lNumber of inputs" : len(self.input.inputs),
            "Camera speed" : self.camera.current_speed_modifier_i,
            "lKey mode" : self.key_mode,
            "Tracked body index" : self.camera.current_tracked_body_index,
            "lModel size type" : self.model_size_type,
            "Camera movement mode" : self.camera.movement_mode,
            "lManual str" : self.key_string,
            "empty" : "   "
        }
        return state

    def run(self):
        while True:
            self.get_time()
            self.check_events()
            self.render()
            self.delta_time = (self.clock.tick(self.framerate) / 1000) * self.physics_speed
            self.camera_delta_time = self.clock.tick(self.framerate)
            pg.display.set_caption(f"Current physics speed : x{self.physics_speed:.2e}")
            self.simulation_time += self.delta_time
            self.display.update(self.get_current_state())
