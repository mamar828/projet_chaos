import numpy as np
import moderngl as mgl
import pywavefront
import struct

from relative_paths import get_path


class Vertex_buffer_object:
    def __init__(self, context):
        self.vertex_buffer_objects = {
            "cube" : Cube_VBO(context),
            "sphere" : Sphere_VBO(context),
            "skybox" : Skybox_VBO(context),
            "cat" : Cat_VBO(context),
            "surface" : Surface_VBO(context)
        }

    def destroy(self):
        [vbo.destroy() for vbo in self.vertex_buffer_objects.values()]


class Base_vertex_buffer_object:
    def __init__(self, context):
        self.context = context
        self.vertex_buffer_object = self.get_vertex_buffer_object()
        self.format: str=None
        self.attrib: list=None
    
    def get_vertex_data(self): ...

    def get_vertex_buffer_object(self):
        return self.context.buffer(self.get_vertex_data())
    
    def destroy(self):
        self.vertex_buffer_object.release()


class Skybox_VBO(Base_vertex_buffer_object):
    def __init__(self, context):
        super().__init__(context)
        self.format = "3f"
        self.attribs = ["in_position"]
    
    @staticmethod
    def get_data(vertices, indices):
        return np.array([vertices[i] for triangle in indices for i in triangle], dtype="f4")

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
        vertex_data = np.flip(vertex_data, 1).copy(order="C")

        return vertex_data


class Cube_VBO(Base_vertex_buffer_object):
    def __init__(self, context):
        super().__init__(context)
        self.format = "2f 3f 3f"
        self.attribs = ["in_texcoord_0", "in_normal", "in_position"]
    
    @staticmethod
    def get_data(vertices, indices):
        return np.array([vertices[i] for triangle in indices for i in triangle], dtype="f4")

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


class External_VBO(Base_vertex_buffer_object):
    def __init__(self, context):
        super().__init__(context)
        self.format = "2f 3f 3f"
        self.attribs = ["in_texcoord_0", "in_normal", "in_position"]

    def get_vertex_data(self, object_path):
        objects = pywavefront.Wavefront(object_path, cache=True, parse=True, create_materials=True)
        obj = objects.materials.popitem()[1]
        return np.array(obj.vertices, dtype="f4")


class Sphere_VBO(External_VBO):
    def get_vertex_data(self):
        return super().get_vertex_data(get_path("objects/sphere/sphere.obj"))


class Cat_VBO(External_VBO):
    def get_vertex_data(self):
        return super().get_vertex_data(get_path("objects/cat/20430_Cat_v1_NEW.obj"))


class Surface_VBO(Base_vertex_buffer_object):
    def __init__(self, context):
        super().__init__(context)
        self.format = "2f"
        self.attribs = ["in_position"]

    def get_vertex_data(self):
        vertices = [(-1, -1), (1, -1), (1, 1), (-1, 1), (-1, -1), (1, 1)]
        vertex_data = struct.pack(f'{len(vertices) * len(vertices[0])}f', *sum(vertices, ()))
        return vertex_data





# class Skybox_VBO(Base_vertex_buffer_object):
#     def __init__(self, context):
#         super().__init__(context)
#         self.format = "3f"
#         self.attribs = ["in_position"]
    
#     @staticmethod
#     def get_data(vertices, indices):
#         return np.array([vertices[i] for triangle in indices for i in triangle], dtype="f4")

#     def get_vertex_data(self):
#         vertices = [
#             (-1,-1, 1), ( 1,-1, 1), ( 1, 1, 1), (-1, 1, 1), # front
#             (-1, 1,-1), (-1,-1,-1), ( 1,-1,-1), ( 1, 1,-1)  # back
#         ]
#         indices = [
#             (0, 2, 3), (0, 1, 2),
#             (1, 7, 2), (1, 6, 7),
#             (6, 5, 4), (4, 7, 6),
#             (3, 4, 5), (3, 5, 0),
#             (3, 7, 4), (3, 2, 7),
#             (0, 6, 1), (0, 5, 6)
#         ]

#         vertex_data = self.get_data(vertices, indices)
#         vertex_data = np.flip(vertex_data, 1).copy(order="C")

#         return vertex_data
