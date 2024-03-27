from pygame.font import SysFont

from src.engines.engine_3D.model import *
from src.engines.engine_3D.relative_paths import get_path

from src.systems.computed_system import ComputedSystem


class Scene:
    def __init__(self, app, scene_objects):
        self.app = app
        self.objects = []
        self.surfaces = []
        self.system = None
        if scene_objects:
            self.load_objects(scene_objects)
        if app.functions:
            self.load_surfaces(app.functions)
        if app.simulation:
            self.system = app.simulation.system
            self.load_simulation()
        self.skybox = Skybox(app)

    def load_objects(self, scene_objects):
        for obj in scene_objects:
            self.objects.append(obj.model(app=self.app, texture_id=obj.texture, scale=obj.scale, rotation=obj.rotation,
                                position=obj.instance.get_position(), instance=obj.instance))
            
    def load_surfaces(self, functions):
        for i, plot_func in enumerate(functions):
            self.surfaces.append(Surface(app=self.app, vertex_array_object_name=f"surface_{i}",
                                         texture_id=plot_func.texture, scale=plot_func.scale,
                                         position=plot_func.position, rotation=plot_func.rotation))
            
    def load_simulation(self):
        # Determine the displayed colors
        if isinstance(self.system, ComputedSystem):
            color_func = lambda body: body.get_color(random_tuple=False)
        else:
            # A lambda function is also created only for consistency
            color_func = lambda body: BaseModel.get_random_color()
        
        for body in self.system.list_of_bodies:
            s = (round(body.mass/(2*10**30), 0) * 30 + 10) / 10
            # s = 2*5*arctan(float(body.mass))/pi
            self.objects.append(Sphere(app=self.app, texture_id=color_func(body), scale=(s,s,s), instance=body,
                                       position=tuple(body.position)))

    def update(self):
        if self.system:
            # Update system
            for i in range(int(self.app.delta_time // self.app.simulation.maximum_delta_time)):
                self.system.update(self.app.simulation.maximum_delta_time)
            self.system.update(self.app.delta_time % self.app.simulation.maximum_delta_time)

            # Update display
            for obj in self.objects:
                if not obj.instance.dead:
                    obj.move(tuple(obj.instance.position))
                else:
                    obj.destroy()
                    self.objects.remove(obj)
        
        else:
            # Keep old methods for legacy
            for obj in self.objects:
                if obj.instance:
                    obj.instance.update(self.app.delta_time)
                    obj.position = obj.instance.get_position()
    
    def destroy(self):
        del self
