from src.engines.engine_2D.models import *

import numpy as np


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
            s = np.round(body.mass/(2*10**30), 0) * 30 + 10
            # s = 2*5*np.arctan(float(body.mass))/np.pi
            self += Circle(screen=self.app.screen, color=Base_model.get_random_color(), scale=(s,s),
                           position=(body.position[0], body.position[1]), instance=body)
    
    def update(self):
        print("delta time", self.app.delta_time)
        # print(self.app.delta_time // 5000)
        # print(self.app.delta_time % 5000)
        for i in range(self.app.delta_time // 100):
            self.system.update(100)
            # print(i)
        self.system.update(self.app.delta_time % 100)
        # if self.app.delta_time >= 10000:
        # self.system.update(self.app.delta_time)
        for obj in self.objects:
            obj.move((obj.instance.position[0], obj.instance.position[1]))
            obj.update()
            # if not obj.instance.fixed:
            #     print(obj.instance.position)
            #     print(obj.instance.velocity)
