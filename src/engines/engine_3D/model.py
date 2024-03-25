import pygame as pg
import moderngl as mgl
import numpy as np
import glm
from relative_paths import get_path


class Base_model:
    def __init__(self, 
            app,
            vertex_array_object_name,
            texture_id,
            position,
            rotation,
            scale,
            instance=None
        ):
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
        self.on_init()

    def update(self):
        self.texture.use(location=0)
        self.program["camPos"].write(self.camera.position)
        self.program["m_view"].write(self.camera.m_view)
        self.program["m_model"].write(self.m_model)

    def update_shadow(self):
        self.shadow_program["m_model"].write(self.m_model)

    def render_shadow(self):
        self.update_shadow()
        self.shadow_vertex_array_object.render()
    
    def on_init(self):
        self.program["m_view_light"].write(self.app.light.m_view_light)
        # resolution
        # self.program["u_resolution"].write(glm.vec2(self.app.window_size))        # Used for shadow smoothing
        # depth texture
        self.depth_texture = self.app.mesh.texture.textures["depth_texture"]
        try: self.program["shadow_map"] = 1
        except Exception: pass
        self.depth_texture.use(location=1)
        # shadow
        try:
            self.shadow_vertex_array_object = self.app.mesh.vertex_array_object.vertex_array_objects[
                                                                            f"shadow_{self.vertex_array_object_name}"]
            self.shadow_program = self.shadow_vertex_array_object.program
            self.shadow_program["m_proj"].write(self.camera.m_proj)
            self.shadow_program["m_view_light"].write(self.app.light.m_view_light)
            self.shadow_program["m_model"].write(self.m_model)
        except Exception: pass
        # texture
        self.texture = self.app.mesh.texture.textures[self.texture_id]
        self.program["u_texture_0"] = 0
        # self.program["texture_width"] = self.texture.width
        # self.program["texture_height"] = self.texture.height
        self.texture.use(location=0)
        # mvp matrices
        self.program["m_proj"].write(self.camera.m_proj)
        self.program["m_view"].write(self.camera.m_view)
        self.program["m_model"].write(self.m_model)
        # light
        self.program["light.position"].write(self.app.light.position)
        self.program["light.Ia"].write(self.app.light.Ia)
        self.program["light.Id"].write(self.app.light.Id)
        self.program["light.Is"].write(self.app.light.Is)

    def get_model_matrix(self):
        # translation
        t_model = glm.translate(glm.mat4(), self.position)
        # rotation
        r_model = glm.rotate(t_model, self.rotation.x, glm.vec3(1,0,0))
        r_model = glm.rotate(r_model, self.rotation.y, glm.vec3(0,1,0))
        r_model = glm.rotate(r_model, self.rotation.z, glm.vec3(0,0,1))
        # scale
        s_model = glm.scale(r_model, self.scale)
        return s_model
    
    def render(self):
        self.update()
        self.vertex_array_object.render()


class Skybox(Base_model):
    def __init__(self,
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


class Animated_model(Base_model):
    def update(self):
        self.m_model = self.get_model_matrix()
        super().update()


class Cube(Animated_model):
    def __init__(self,
            app,
            texture_id,
            position=(0,0,0),
            rotation=(0,0,0),
            scale=(1,1,1),
            instance=None
        ):
        super().__init__(app, "cube", texture_id, position, rotation, scale, instance)


class Surface(Animated_model):
    def __init__(self,
            app,
            texture_id,
            position=(0,10,0),
            rotation=(0,0,0),
            scale=(5,5,5),
            instance=None
        ):
        super().__init__(app, "surface", texture_id, position, rotation, scale, instance)


class Sphere(Animated_model):
    def __init__(self,
            app,
            texture_id,
            position=(0,0,0),
            rotation=(0,0,0),
            scale=(1,1,1),
            instance=None
        ):
        super().__init__(app, "sphere", texture_id, position, rotation, self.convert_scale(scale), instance)
    
    def convert_scale(self, scale):
        # Convert the object's scale in the default dimensions
        return tuple(np.array(scale)*0.009095)


class Cat(Base_model):
    def __init__(self,
            app,
            position=(0,0,0),
            rotation=(0,0,0),
            scale=(1,1,1),
            instance=None
        ):
        super().__init__(app, "cat", "cat", position, rotation, scale, instance)



class Surfacenooooo:#(Base_model):
    def __init__(self,
            app,
            texture_id="surface",
            position=(0,20,0),
            rotation=(0,0,0),
            scale=(1,1,1)
        ):
        self.app = app
        self.instance = None
        self.position = position
        self.context = app.context
        self.vbo = self.get_vbo()
        self.shader_program = self.get_shader_program()
        self.vao = self.get_vao()
        self.m_model = self.get_model_matrix()
        self.texture = self.get_texture(get_path("textures/floor_test.png"))
        self.on_init()
    
    def update(self):
        self.texture.use(location=0)
        # self.shader_program["camPos"].write(self.camera.position)
        self.shader_program["m_view"].write(self.app.camera.m_view)
        self.shader_program["m_model"].write(self.m_model)

    def get_model_matrix(self):
        # translation
        return glm.translate(glm.mat4(), self.position)

    def get_texture(self, path):
        texture = pg.image.load(path).convert()
        texture = pg.transform.flip(pg.image.load(path).convert(), flip_x=False, flip_y=True)
        # texture.fill("green")
        texture = self.context.texture(size=texture.get_size(), components=3, data=pg.image.tostring(texture, "RGB"))
        # mipmaps activation (correction for high distance objects)
        texture.filter = (mgl.NEAREST, mgl.NEAREST)
        # texture.filter = (mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR)       # alternative mipmap
        texture.build_mipmaps()
        texture.anisotropy = 32.0
        return texture
    
    def get_model_matrix(self):
        return glm.mat4()

    def on_init(self):
        # texture
        self.shader_program["u_texture_0"] = 0
        self.texture.use()
        self.shader_program["m_proj"].write(self.app.camera.m_proj)
        self.shader_program["m_view"].write(self.app.camera.m_view)
        self.shader_program["m_model"].write(self.m_model)

    def render(self):
        self.update()
        self.vao.render()
    
    def destroy(self):
        self.vao.release()
        self.vbo.release()
        self.shader_program.release()

    def get_vao(self):
        return self.context.vertex_array(self.shader_program, [(self.vbo, "3f", "in_position")],
                                         skip_errors=True)
    
    def get_vertex_data(self):
        vertices = [
            (-1,-1, 1), ( 1,-1, 1), ( 1, 1, 1), (-1, 1, 1), # front
            (-1, 1,-1), (-1,-1,-1), ( 1,-1,-1), ( 1, 1,-1)  # back
        ]
        indices = [
            (0, 2, 3), (0, 1, 2),
            (1, 7, 2), (1, 6, 7),
            (6, 5, 4), (4, 7, 6),
            (3, 4, 5), (3, 5, 0),
            (3, 7, 4), (3, 2, 7),
            (0, 6, 1), (0, 5, 6)
        ]

        vertex_data = self.get_data(vertices, indices)

        # Texture related data
        tex_coord_vertices = [(0,0), (1,0), (1,1), (0,1)]
        tex_coord_indices = [
            (0,2,3), (0,1,2),
            (0,2,3), (0,1,2),
            (0,1,2), (2,3,0),
            (2,3,0), (2,0,1),
            (0,2,3), (0,1,2),
            (3,1,2), (3,0,1)
        ]
        tex_coord_data = self.get_data(tex_coord_vertices, tex_coord_indices)

        # Lighting on all the different faces
        normals = np.array(
            [( 0, 0, 1) * 6,
             ( 1, 0, 0) * 6,
             ( 0, 0,-1) * 6,
             (-1, 0, 0) * 6,
             ( 0, 1, 0) * 6,
             ( 0,-1, 0) * 6],
             dtype="f4"
        ).reshape(36,3)

        return np.hstack([tex_coord_data, normals, vertex_data])
    
    @staticmethod
    def get_data(vertices, indices):
        return np.array(
            [vertices[ind] for triangle in indices for ind in triangle],
            dtype="f4"
        )

    def get_vbo(self):
        return self.context.buffer(self.get_vertex_data())
    
    def get_shader_program(self):
        with open(get_path(f"shaders/surface.vert")) as file:
            vertex_shader = file.read()

        with open(get_path(f"shaders/surface.frag")) as file:
            fragment_shader = file.read()

        return self.context.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)


class Surface_CHAT:
    def __init__(self, app, texture_id="surface", position=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1)):
        self.app = app
        self.instance = None
        self.position = position
        self.context = app.context
        self.vbo = self.get_vbo()
        self.shader_program = self.get_shader_program()
        self.vao = self.get_vao()
        self.texture = self.get_texture(get_path("textures/floor_test.png"))
        self.on_init()

    def update(self):
        self.texture.use(location=0)
        self.shader_program["m_proj"].write(self.app.camera.m_proj)
        self.shader_program["m_view"].write(self.app.camera.m_view)
        self.shader_program["m_model"].write(self.get_model_matrix())

    def get_model_matrix(self):
        return glm.translate(glm.mat4(), self.position)

    def get_texture(self, path):
        texture = pg.image.load(path).convert()
        texture = pg.transform.flip(pg.image.load(path).convert(), flip_x=False, flip_y=True)
        # texture.fill("green")
        texture = self.context.texture(size=texture.get_size(), components=3, data=pg.image.tostring(texture, "RGB"))
        # mipmaps activation (correction for high distance objects)
        texture.filter = (mgl.NEAREST, mgl.NEAREST)
        # texture.filter = (mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR)       # alternative mipmap
        texture.build_mipmaps()
        texture.anisotropy = 32.0
        return texture

    def on_init(self):
        # Texture setup code...
        self.shader_program["u_texture_0"] = 0
        self.texture.use()

    def render(self):
        self.update()
        self.vao.render()

    def destroy(self):
        self.vao.release()
        self.vbo.release()
        self.shader_program.release()

    def get_vao(self):
        return self.context.vertex_array(self.shader_program, [(self.vbo, "3f 2f", "in_position", "in_texcoord_0")])

    def get_vertex_data(self):
        vertices = [
            (-1.0, 0.0, -1.0), (1.0, 0.0, -1.0), (1.0, 0.0, 1.0), (-1.0, 0.0, 1.0)
        ]
        tex_coords = [
            (0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)
        ]
        indices = [(0, 1, 2), (0, 2, 3)]

        vertex_data = np.array([vertices[i] + tex_coords[i] for face in indices for i in face], dtype="f4")
        return vertex_data

    def get_vbo(self):
        return self.context.buffer(self.get_vertex_data())

    def get_shader_program(self):
        with open(get_path(f"shaders/surface.vert")) as file:
            vertex_shader = file.read()

        with open(get_path(f"shaders/surface.frag")) as file:
            fragment_shader = file.read()

        return self.context.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)







    # def __init__(self,
    #         app,
    #         texture_id="surface",
    #         position=(0,10,0),
    #         rotation=(0,0,0),
    #         scale=(1,1,1)
    #     ):
    #     super().__init__(app, "surface", texture_id, position, rotation, scale)
    #     self.on_init()

    # def on_init(self):
    #     # texture
    #     self.texture = self.app.mesh.texture.textures[self.texture_id]
    #     self.program["u_texture_0"] = 0
    #     self.texture.use(location=0)
    #     # mvp matrices
    #     self.program["m_proj"].write(self.camera.m_proj)
    #     self.program["m_view"].write(glm.mat4(glm.mat3(self.camera.m_view)))

    # def update(self):
    #     self.program["m_view"].write(glm.mat4(glm.mat3(self.camera.m_view)))






class Surface_bad:
    def __init__(self,
            app,
            texture_id
        ):
        self.app = app
        # self.m_model = self.get_model_matrix()
        self.texture_id = texture_id
        self.vertex_array_object = app.mesh.vertex_array_object.vertex_array_objects["surface"]
        self.vertex_array_object_name = "surface"
        self.program = self.vertex_array_object.program
        self.camera = self.app.camera
        self.on_init()

    def update(self):
        self.texture.use(location=0)
        self.program["camPos"].write(self.camera.position)
        self.program["m_view"].write(self.camera.m_view)
        self.program["m_model"].write(self.m_model)

    def on_init(self):
        # self.program["m_view_light"].write(self.app.light.m_view_light)
        # resolution
        # self.program["u_resolution"].write(glm.vec2(self.app.window_size))        # Used for shadow smoothing
        # depth texture
        # self.depth_texture = self.app.mesh.texture.textures["depth_texture"]
        # self.program["shadow_map"] = 1
        # self.depth_texture.use(location=1)
        # # shadow
        # self.shadow_vertex_array_object = self.app.mesh.vertex_array_object.vertex_array_objects[
        #                                                                 f"shadow_{self.vertex_array_object_name}"]
        # self.shadow_program = self.shadow_vertex_array_object.program
        # self.shadow_program["m_proj"].write(self.camera.m_proj)
        # self.shadow_program["m_view_light"].write(self.app.light.m_view_light)
        # self.shadow_program["m_model"].write(self.m_model)
        # texture
        # self.texture = self.app.mesh.texture.textures[self.texture_id]
        # self.program["u_texture_0"] = 0
        # self.program["texture_width"] = self.texture.width
        # self.program["texture_height"] = self.texture.height
        # self.texture.use(location=0)
        # mvp matrices
        # self.program["m_proj"].write(self.camera.m_proj)
        # self.program["m_view"].write(self.camera.m_view)
        # self.program["m_model"].write(self.m_model)
        # light
        # self.program["light.position"].write(self.app.light.position)
        # self.program["light.Ia"].write(self.app.light.Ia)
        # self.program["light.Id"].write(self.app.light.Id)
        # self.program["light.Is"].write(self.app.light.Is)

        self.program['u_resolution'] = self.app.window_size

    def get_model_matrix(self):
        return glm.mat4()
    

        # translation
        t_model = glm.translate(glm.mat4(), self.position)
        # rotation
        r_model = glm.rotate(t_model, self.rotation.x, glm.vec3(1,0,0))
        r_model = glm.rotate(r_model, self.rotation.y, glm.vec3(0,1,0))
        r_model = glm.rotate(r_model, self.rotation.z, glm.vec3(0,0,1))
        # scale
        s_model = glm.scale(r_model, self.scale)
        return s_model
    
    def render(self):
        self.update()
        self.vertex_array_object.render()

