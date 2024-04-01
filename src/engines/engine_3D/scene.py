from pygame.font import SysFont

from src.engines.engine_3D.models import *
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
        self.current_i = 0

    def load_objects(self, scene_objects):
        for obj in scene_objects:
            if obj.instance:
                self.objects.append(obj.model(app=self.app, texture_id=obj.texture, scale=obj.scale,
                                   rotation=obj.rotation, position=obj.instance.get_position(), instance=obj.instance))
            else:
                self.objects.append(obj.model(app=self.app, texture_id=obj.texture, scale=obj.scale,
                                   rotation=obj.rotation, position=obj.position))
            
    def load_surfaces(self, functions):
        for i, surface in enumerate(functions):
            self.surfaces.append(Surface(app=self.app, vertex_array_object_name=f"surface_{i}",
                                         texture_id=surface.texture, scale=surface.scale, position=surface.position,
                                         rotation=surface.rotation, instance=surface.instance))
            
    def load_simulation(self):
        # Determine the displayed colors
        if isinstance(self.system, ComputedSystem):
            color_func = lambda body: body.get_color(random_tuple=False)
        else:
            # A lambda function is also created only for consistency
            color_func = lambda body: BaseModel.get_random_color()
        
        for body in self.system.list_of_bodies:
            s = (round(body.mass/(2*10**30), 0) * 30 + 10) / 10
            self.objects.append(Sphere(app=self.app, texture_id=color_func(body), scale=(s,s,s), instance=body,
                                       position=tuple(body.position), saturated=True))

    def update(self):
        if self.system:
            # Update system
            for i in range(int(self.app.delta_time // self.app.simulation.maximum_delta_time)):
                self.system.update(self.app.simulation.maximum_delta_time)
            self.system.update(self.app.delta_time % self.app.simulation.maximum_delta_time)

            # Update objects on display
            for obj in self.objects:
                if obj.instance:
                    if not obj.instance.dead:
                        obj.move(tuple(obj.instance.position))
                    else:
                        obj.destroy()
                        self.objects.remove(obj)

            # Update surfaces on display only once every 10 updates
            # self.current_i += 1
            # if self.current_i > 10:
            #     self.current_i = 0
            #     for i, surface in enumerate(self.app.functions):
            #         if surface.instance:
            #             surface.update()
            #             vbo = self.app.mesh.vertex_array_object.vertex_buffer_object.vertex_buffer_objects[f"surface_{i}"]
            #             vbo.write(surface.get_vertex_data().tobytes())  # Update VBO with new vertex data

            #             # Rebind VAO with updated VBO
            #             self.app.mesh.vertex_array_object.vertex_array_objects[f"surface_{i}"] = self.app.mesh.vertex_array_object.get_vertex_array_object(
            #                 program=self.app.mesh.vertex_array_object.program.programs["surface"],
            #                 vertex_buffer_object=vbo
            #             )
            #             # self.app.mesh.vertex_array_object.vertex_buffer_object.vertex_buffer_objects[
            #             #                                                                     f"surface_{i}"].update()
            #             # self.app.mesh.vertex_array_object.vertex_array_objects[f"surface_{i}"] = self.app.mesh.vertex_array_object.get_vertex_array_object(
            #             #     program=self.app.mesh.vertex_array_object.program.programs["surface"],
            #             #     vertex_buffer_object=self.app.mesh.vertex_array_object.vertex_buffer_object.vertex_buffer_objects[f"surface_{i}"]
            #             # )

        else:
            # Keep old methods for legacy
            for obj in self.objects:
                if obj.instance:
                    obj.instance.update(self.app.delta_time)
                    obj.position = obj.instance.get_position()
    
    def destroy(self):
        del self
