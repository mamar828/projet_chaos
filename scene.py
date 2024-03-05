import pygame as pg


class Scene:
    def __init__(self, app, scene_objects):
        self.app = app
        self.objects = []
        self.load(scene_objects)

    def add_object(self, object):
        self.objects.append(object)

    def __iadd__(self, object):
        self.add_object(object)
        return self    

    def load(self, scene_objects):
        for obj in scene_objects:
            self += obj["model"](screen=self.app.screen, color=obj["color"], scale=obj["scale"],
                                 position=obj["object_instance"].get_position(), instance=obj["object_instance"])
    
    def update(self):
        for obj in self.objects:
            if obj.instance:
                obj.instance.update(self.app.delta_time)
                obj.move(obj.instance.get_position())
                obj.update()




    # {"object_instance": Flat_earth(position=(2,2)), "model": Rectangle, "texture_id": "blue", "scale": (1,1)}
