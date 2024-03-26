from model import *
from relative_paths import get_path


class Scene:
    def __init__(self, app, scene_objects):
        self.app = app
        self.objects = []
        self.surfaces = []
        if scene_objects:
            self.load_objects(scene_objects)
        if app.functions:
            self.load_surfaces(app.functions)
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

    def update(self):
        for obj in self.objects:
            if obj.instance:
                obj.instance.update(self.app.delta_time)
                obj.position = obj.instance.get_position()
    
    def destroy(self):
        del self
