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
        self.function = np.vectorize(lambda x, y: np.sin(x)*np.sin(y) * 2)
        super().__init__(context)
        # self.format = "2f"
        # self.format = "2f 3f 3f"
        self.format = "2f 3f"
        # self.attribs = ["in_position"]
        # self.attribs = ["in_texcoord_0", "in_normal", "in_position"]
        self.attribs = ["in_texcoord_0", "in_position"]

    @staticmethod
    def get_data(vertices, indices):
        return np.array([vertices[i] for triangle in indices for i in triangle], dtype="f4")
    
    def get_vertex_data(self):
        x_num, y_num = 100, 100
        x_start, y_start = -200, -200
        x_end, y_end = 200, 200
        x_space = np.linspace(x_start, x_end, x_num)
        y_space = np.linspace(y_start, y_end, y_num)
        x, y = np.meshgrid(x_space, y_space)
        z_array = self.function(x, y)

        vertices = []
        indices = []
        for i in range(x_num):
            for j in range(y_num):
                zero = i + j*x_num
                vertices.append((i/(x_num-1) * (x_end - x_start) + x_start, z_array[i,j],
                                 j/(y_num-1) * (y_end - y_start) + y_start))
                if i < x_num-1 and j < y_num-1:
                    indices.append((zero, zero + x_num+1, zero + x_num))
                    indices.append((zero, zero + 1,  zero + x_num+1))
                    # Create other side
                    indices.append((zero, zero + x_num, zero + x_num+1))
                    indices.append((zero, zero + x_num+1, zero + 1))

        vertex_data = self.get_data(vertices, indices)

        tex_coord_vertices = [(0,0), (1,0), (1,1), (0,1)]
        tex_coord_indices = [
            (0,2,3), (0,1,2), (0,3,2), (0,2,1)
        ] * int((len(indices) / 4))
        tex_coord_data = self.get_data(tex_coord_vertices, tex_coord_indices)

        return np.hstack([tex_coord_data, vertex_data])


    def get_vertex_data_non_functional(self, resolution=10):
        # Generate a grid of points in the x-y plane
        x = np.linspace(-1, 1, resolution)
        y = np.linspace(-1, 1, resolution)
        xx, yy = np.meshgrid(x, y)

        # Evaluate the function to get z-coordinate for each point in the grid
        zz = self.function(xx, yy)

        # Ensure that zz has the same shape as xx and yy
        zz = zz[:resolution, :resolution]

        # Reshape the coordinates into a single array
        vertices = np.vstack([xx.flatten(), yy.flatten(), zz.flatten()]).T

        # Ensure vertices array is C-contiguous
        vertices = np.ascontiguousarray(vertices)

        # Define texture coordinates (you can adjust this based on your needs)
        tex_coords = np.mgrid[0:resolution, 0:resolution].reshape(2,-1).T.astype(np.float32) / resolution

        # Ensure texture coordinates array is C-contiguous
        tex_coords = np.ascontiguousarray(tex_coords)

        # Concatenate vertices data
        vertex_data = np.hstack([tex_coords, vertices])

        return vertex_data

    def get_vertex_data_plane(self):
        # Define vertices for a plane (two triangles)
        vertices = [
            (-1.0, -1.0, -1.0),  # Bottom-left
            (1.0, -1.0, -1.0),   # Bottom-right
            (1.0, 1.0, 1.0),    # Top-right
            (-1.0, 1.0, 1.0),   # Top-left
        ]

        # Texture coordinates
        tex_coord_data = [
            (0.0, 0.0),  # Bottom-left
            (1.0, 0.0),  # Bottom-right
            (1.0, 1.0),  # Top-right
            (0.0, 1.0),  # Top-left
        ]

        # Define indices for the two triangles (clockwise winding order)
        indices = [
            (0, 1, 2),  # Triangle 1 (bottom-right-top)
            (0, 2, 3),  # Triangle 2 (bottom-left-top)
            (0, 2, 1),  # Triangle 3 (bottom-left-top) - Back face
            (0, 3, 2),  # Triangle 4 (top-right-bottom) - Back face
        ]

        # Concatenate vertices data
        vertex_data = np.array([tex_coord_data[i] + vertices[i] for triangle in indices for i in triangle], dtype="f4")

        return vertex_data

    def get_vertex_data_cube(self):
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
        # return vertex_data

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

        return np.hstack([tex_coord_data, vertex_data])


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
    def get_data_CHAT(vertices, normals, indices):
        return np.array([vertices[i] + normals[i] for triangle in indices for i in triangle], dtype="f4")
    
    def get_vertex_data_CHAT(self):
        # Define vertices for a plane (two triangles)
        vertices = [
            (-1.0, -1.0, 0.0),  # Bottom-left
            (1.0, -1.0, 0.0),   # Bottom-right
            (1.0, 1.0, 0.0),    # Top-right
            (-1.0, 1.0, 0.0),   # Top-left
        ]
        # Define indices for the two triangles
        indices = [
            (0, 1, 2),  # Triangle 1
            (0, 2, 3),  # Triangle 2
        ]

        # Normals for lighting (one normal for each vertex)
        normals = [
            (0.0, 0.0, 1.0),  # Normal facing towards positive z-axis
            (0.0, 0.0, 1.0),  # Normal facing towards positive z-axis
            (0.0, 0.0, 1.0),  # Normal facing towards positive z-axis
            (0.0, 0.0, 1.0),  # Normal facing towards positive z-axis
        ]

        vertex_data = self.get_data(vertices, normals, indices)

        # Texture coordinates
        tex_coord_data = np.array([
            (0.0, 0.0),  # Bottom-left
            (1.0, 0.0),  # Bottom-right
            (1.0, 1.0),  # Top-right
            (0.0, 1.0),  # Top-left
        ], dtype="f4")

        return np.hstack([tex_coord_data, vertex_data])


    # def get_vertex_data(self):
    #     self.amplitude = 100
    #     self.frequency = 10
    #     self.resolution = (300,300)
    #     vertices = []
    #     normals = []

    #     # Generate vertices and normals
    #     for i in range(self.resolution[0]):
    #         for j in range(self.resolution[1]):
    #             # Calculate x, y, z coordinates based on sine function parameters
    #             x = i / (self.resolution[0] - 1) * 2 - 1
    #             y = j / (self.resolution[1] - 1) * 2 - 1
    #             z = self.amplitude * np.sin(self.frequency * (x + y))
    #             vertices.extend([x, y, z])

    #             # Calculate normals (approximation using neighboring vertices)
    #             dx = self.amplitude * self.frequency * np.cos(self.frequency * (x + y))
    #             dy = self.amplitude * self.frequency * np.cos(self.frequency * (x + y))
    #             dz = 1.0
    #             length = np.sqrt(dx ** 2 + dy ** 2 + dz ** 2)
    #             normals.extend([dx / length, dy / length, dz / length])

    #     return np.array(vertices + normals, dtype="f4")
    
    # def get_vao(self):
    #     return self.context.vertex_array(self.shader_program, [(self.vbo, "3f 3f", "in_position", "in_normal")])

    #     vertices = [(-1, -1), (1, -1), (1, 1), (-1, 1), (-1, -1), (1, 1)]
    #     vertex_data = struct.pack(f'{len(vertices) * len(vertices[0])}f', *sum(vertices, ()))
    #     return vertex_data
    




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
