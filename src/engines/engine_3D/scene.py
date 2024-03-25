from model import *
from relative_paths import get_path


class Scene:
    def __init__(self, app, scene_objects, plot_function=False):
        self.app = app
        self.objects = []
        self.load(scene_objects)
        self.skybox = Skybox(app)
        self.function = None
        if plot_function:
            self.plot_function()

    def add_object(self, object):
        self.objects.append(object)

    def __iadd__(self, object):
        self.add_object(object)
        return self
    
    def load(self, scene_objects):
        for obj in scene_objects:
            self += obj["model"](app=self.app, texture_id=obj["color"], scale=obj["scale"],
                                 position=obj["object_instance"].get_position(), instance=obj["object_instance"])

    def update(self):
        for obj in self.objects:
            if obj.instance:
                obj.instance.update(self.app.delta_time)
                obj.position = obj.instance.get_position()
    
    def destroy(self):
        del self
    
    def plot_function(self):
        self.function = Surface(app=self.app, texture_id="green")



class Scene_test:
    def __init__(self, app, scene_elements):
        self.app = app
        self.objects = []
        self.load()
        # self.load(scene_elements)
        self.skybox = Skybox(app)

    def add_object(self, object):
        self.objects.append(object)

    def __iadd__(self, object):
        self.add_object(object)
        return self
    
    def load(self):
        app = self.app
        add = self.add_object

        n = 20
        offset = 0
        # for x in range(-n,n+1,2):
        #     for z in range(-n,n+1,2):
        #         add(Cube(app, 4, (x,0,z-offset)))
        # for x in range(-n,n+1,2):
        #     for y in range(0,n+1,2):
        #         add(Cube(app, 4, (x,y,-n)))
        for z in range(-50,55,5):
            for x in range(-50,55,5):
                for y in range(-50,55,5):
                    add(Cube(app, texture_id=3, position=(x,y,z), rotation=(
                            np.random.randint(0,360),
                            np.random.randint(0,360),
                            np.random.randint(0,360)
                        ), scale=(
                            np.random.rand()*2,
                            np.random.rand()*2,
                            np.random.rand()*2
                        )))
        # add(Cube(app, texture_id=1, position=(0,6,0), scale=(1,5,1)))
        # [add(Cube(app, texture_id=3, position=(2,y,0))) for y in range(2,12,2)]
        # self.moving_cube = Cube(app, texture_id=2, position=(0,10,-10), scale=(1,1,1))
        # add(self.moving_cube)
        # add(Cube(app, texture_id=0, position=self.app.light.position))
        # add(Sphere(app, texture_id=0, position=(10,2,0)))#, scale=(0.009095*(1+98),0.009095*(1+98),0.009095*(1+98))))
        # for i in range(2,102,2):
        #     self += Cube(app, texture_id="yellow", position=(8,i,0))
        # add(Cat(app, position=(0,0,0), rotation=(-90,0,0), scale=(50,50,50)))


    def update(self):
        pass
        # self.moving_cube.position = update_position(self.moving_cube.position, self.app.time)

def update_position(position, time):
    return position[0], np.sin(time)*3 + 10, np.cos(time)*3 + 5
