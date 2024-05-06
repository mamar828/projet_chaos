from pygame.font import SysFont
from astropy.constants import M_sun, M_earth, R_sun, R_earth

from src.engines.engine_3D.models import *

from src.systems.computed_system import ComputedSystem
from src.bodies.fake_body import FakeBody


class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = []
        self.surfaces = []
        self.hidden_surfaces = []
        self.system = None
        if app.objects:
            self.load_objects(app.objects)
        if app.functions:
            self.load_surfaces(app.functions)
        if app.simulation:
            self.system = app.simulation.system
            self.load_simulation()
        self.skybox = Skybox(app)
        self.current_tick = 0
        self.total_ticks = 0

    def load_objects(self, objects):
        for obj in objects:
            if obj.instance:
                self.objects.append(obj.model(app=self.app, texture_id=obj.texture, scale=obj.scale,
                                   rotation=obj.rotation, position=obj.instance.get_position(), instance=obj.instance))
            else:
                self.objects.append(obj.model(app=self.app, texture_id=obj.texture, scale=obj.scale,
                                   rotation=obj.rotation, position=obj.position))
            
    def load_surfaces(self, functions):
        for i, surface in enumerate(functions):
            surf = Surface(app=self.app, vertex_array_object_name=f"surface_{i}",
                           texture_id=surface.texture, scale=surface.scale, position=surface.position,
                           rotation=surface.rotation, instance=surface.instance)
            if not surface.hidden:
                self.surfaces.append(surf)
            else:
                self.hidden_surfaces.append(surf)
            
    def load_simulation(self):
        # Determine the displayed colors
        if isinstance(self.system, ComputedSystem):
            color_func = lambda body: body.get_color(random_tuple=False)
        else:
            # A lambda function is also created only for consistency
            color_func = lambda body: BaseModel.get_random_color()
        
        for body in self.system.list_of_bodies:
            if self.app.model_size_type == "exaggerated":
                s = (round(body.mass/(2*10**30), 0) * 30 + 10) / 10
                if body.mass == 1:
                    s *= 0.5
            else:
                if abs(body.mass - M_sun.value) < 1e28:
                    # Hard code sun size
                    s = R_sun.value / 10**(self.app.simulation.system.n)
                elif abs(body.mass - M_earth.value) < 1e22:
                    # Hard code earth size
                    s = R_earth.value / 10**(self.app.simulation.system.n)
                elif abs(body.mass - 0.07346e24) < 1e10:
                    # Hard code moon size
                    s = 1737e3 / 10**(self.app.simulation.system.n)
                else:
                    s = R_earth.value / 10**(self.app.simulation.system.n) / 2
            if isinstance(body, FakeBody):
                self.objects.append(Sphere(app=self.app, texture_id="grey", scale=(s,s,s), instance=body,
                                        position=tuple(body.position), saturated=self.app.saturated))
            else:
                self.objects.append(Sphere(app=self.app, texture_id=color_func(body), scale=(s,s,s), instance=body,
                                           position=tuple(body.position),
                                           saturated=self.app.saturated if body.mass < 1e29 else True))

    def update(self):
        if self.system:
            # Update system
            self.current_tick += self.app.delta_time
            self.total_ticks += self.app.delta_time
            for i in range(int(self.current_tick // self.app.simulation.maximum_delta_time)):
                self.system.update(self.app.simulation.maximum_delta_time)
                self.current_tick -= self.app.simulation.maximum_delta_time

            # Update objects on display
            for obj in self.objects:
                if obj.instance:
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
