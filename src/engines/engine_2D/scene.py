from src.engines.engine_2D.models import *


class Scene:
    def __init__(self, app, system):
        self.app = app
        self.system = system
        self.objects = []
        self.load(system)

    def add_object(self, object):
        self.objects.append(object)

    def __iadd__(self, object):
        self.add_object(object)
        return self    

    def load(self, system):
        for body in system.list_of_bodies:
            s = body.mass*5
            self += Circle(screen=self.app.screen, color=Base_model.get_random_color(), scale=(s,s),
                           position=(body.position[0], body.position[1]), instance=body)
    
    def update(self):
        self.system.update(self.app.delta_time)
        for obj in self.objects:
            obj.move((obj.instance.position[0], obj.instance.position[1]))
            obj.update()
            if not obj.instance.fixed:
                print(obj.instance.position)
                print(obj.instance.velocity)
