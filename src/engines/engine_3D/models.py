from numpy import array as nparray
from random import choice
import glm


class BaseModel:
    def __init__(
            self, 
            app,
            vertex_array_object_name,
            texture_id,
            position,
            rotation,
            scale,
            instance=None,
            saturated=False
        ):
        if saturated and not vertex_array_object_name.startswith("surface"):
            vertex_array_object_name = f"saturated_{vertex_array_object_name}"

        self.app = app
        self.position = position
        self.rotation = glm.vec3([glm.radians(angle) for angle in rotation])  # Convert angles from degrees to radians
        self.scale = scale
        self.m_model = self.get_model_matrix()
        self.texture_id = texture_id
        self.vertex_array_object = app.mesh.vertex_array_object.vertex_array_objects[vertex_array_object_name]
        self.vertex_array_object_name = vertex_array_object_name
        self.program = self.vertex_array_object.program
        self.camera = self.app.camera
        self.instance = instance
        self.saturated = saturated
        self.on_init()

    def update(self):
        self.texture.use(location=0)
        if not self.saturated: self.program["camPos"].write(self.camera.position)
        self.program["m_view"].write(self.camera.m_view)
        self.program["m_model"].write(self.m_model)

    def update_shadow(self):
        self.shadow_program["m_model"].write(self.m_model)

    def render_shadow(self):
        self.update_shadow()
        self.shadow_vertex_array_object.render()
    
    def on_init(self):
        self.shadow_program = None
        if not self.saturated:
            # Initialize shadow and light concerned parameters
            self.program["m_view_light"].write(self.app.light.m_view_light)
            self.program["shadow_map"] = 1
            # resolution
            # self.program["u_resolution"].write(glm.vec2(self.app.window_size))        # Used for shadow smoothing
            # depth texture
            # shadow
            self.shadow_vertex_array_object = self.app.mesh.vertex_array_object.vertex_array_objects[
                                                                            f"shadow_{self.vertex_array_object_name}"]
            self.shadow_program = self.shadow_vertex_array_object.program
            self.shadow_program["m_proj"].write(self.camera.m_proj)
            self.shadow_program["m_view_light"].write(self.app.light.m_view_light)
            self.shadow_program["m_model"].write(self.m_model)
            # light
            self.program["light.position"].write(self.app.light.position)
            self.program["light.Ia"].write(self.app.light.Ia)
            self.program["light.Id"].write(self.app.light.Id)
            self.program["light.Is"].write(self.app.light.Is)

        self.depth_texture = self.app.mesh.texture.textures["depth_texture"]
        self.depth_texture.use(location=1)
        # texture
        self.texture = self.app.mesh.texture.textures[self.texture_id]
        self.program["u_texture_0"] = 0
        self.texture.use(location=0)
        # mvp matrices
        self.program["m_proj"].write(self.camera.m_proj)
        self.program["m_view"].write(self.camera.m_view)
        self.program["m_model"].write(self.m_model)

    def get_model_matrix(self):
        # translation 
        # Account for the fact that usual coords are (x,y,z) but model ones should be (x,z,y)
        t_model = glm.translate(glm.mat4(), (self.position[0], self.position[2], -self.position[1]))
        # rotation
        r_model = glm.rotate(t_model, self.rotation.x, glm.vec3(1,0,0))
        r_model = glm.rotate(r_model, self.rotation.y, glm.vec3(0,0,1))
        r_model = glm.rotate(r_model, self.rotation.z, glm.vec3(0,1,0))
        # scale
        s_model = glm.scale(r_model, (self.scale[0], self.scale[2], self.scale[1]))
        return s_model
    
    def render(self):
        self.update()
        self.vertex_array_object.render()

    def move(self, position: tuple[float,float,float]):
        self.position = position

    def destroy(self):
        del self
    
    @staticmethod
    def get_random_color():
        # black removed
        return choice(["green", "red", "blue", "yellow", "orange", "cyan", "magenta", "white", "purple",
                       "brown", "grey"])


class Skybox(BaseModel):
    def __init__(
            self,
            app,
            texture_id="skybox",
            position=(0,0,0),
            rotation=(0,0,0),
            scale=(1,1,1)
        ):
        super().__init__(app, "skybox", texture_id, position, rotation, scale)
        self.on_init()

    def on_init(self):
        # texture
        self.texture = self.app.mesh.texture.textures[self.texture_id]
        self.program["u_texture_skybox"] = 0
        self.texture.use(location=0)
        # mvp matrices
        self.program["m_proj"].write(self.camera.m_proj)
        self.program["m_view"].write(glm.mat4(glm.mat3(self.camera.m_view)))

    def update(self):
        self.program["m_view"].write(glm.mat4(glm.mat3(self.camera.m_view)))


class AnimatedModel(BaseModel):
    def update(self):
        self.m_model = self.get_model_matrix()
        super().update()


class Cube(AnimatedModel):
    def __init__(
            self,
            app,
            texture_id,
            position=(0,0,0),
            rotation=(0,0,0),
            scale=(1,1,1),
            instance=None,
            saturated=False
        ):
        super().__init__(app, "cube", texture_id, position, rotation, scale, instance, saturated)


class Surface(BaseModel):
    def __init__(
            self,
            app,
            vertex_array_object_name,
            texture_id,
            position=(0,0,0),
            rotation=(0,0,0),
            scale=(1,1,1),
            instance=None
        ):
        super().__init__(app, vertex_array_object_name, texture_id, position, rotation, scale, instance, True)


class Sphere(AnimatedModel):
    def __init__(
            self,
            app,
            texture_id,
            position=(0,0,0),
            rotation=(0,0,0),
            scale=(1,1,1),
            instance=None,
            saturated=False
        ):
        super().__init__(app, "sphere", texture_id, position, rotation, self.convert_scale(scale), instance, saturated)
    
    def convert_scale(self, scale):
        # Convert the object's scale in the default dimensions
        return tuple(nparray(scale)*0.009095)


class Cat(BaseModel):
    def __init__(
            self,
            app,
            position=(0,0,0),
            rotation=(0,0,0),
            scale=(1,1,1),
            instance=None,
            saturated=False,
            texture_id="cat"
        ):
        super().__init__(app, "cat", texture_id, position, rotation, scale, instance, saturated)
