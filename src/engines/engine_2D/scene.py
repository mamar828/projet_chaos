from src.engines.engine_2D.models import *

# from numpy import arctan, pi


class Scene:
    def __init__(self, app):
        self.app = app
        self.system = app.simulation.system
        self.objects = []
        self.load()

    def add_object(self, object):
        self.objects.append(object)

    def __iadd__(self, object):
        self.add_object(object)
        return self

    def load(self):
        for body, plot_trace in zip(self.system.list_of_bodies, self.app.simulation.traces):
            s = round(body.mass/(2*10**30), 0) * 30 + 10
            # s = 2*5*arctan(float(body.mass))/pi
            self += Circle(screen=self.app.screen, color=Base_model.get_random_color(), scale=(s,s),
                           position=(body.position[0], body.position[1]), instance=body, plot_trace=plot_trace)
    
    def update(self):
        # Update system
        print(self.app.delta_time)
        for i in range(self.app.delta_time // 100):
            self.system.update(100)
        self.system.update(self.app.delta_time % 100)

        # Update display
        for obj in self.objects:
            obj.move((obj.instance.position[0], obj.instance.position[1]))
            obj.update()
