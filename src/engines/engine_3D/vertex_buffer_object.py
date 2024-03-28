import numpy as np
from pywavefront import Wavefront
from gzip import open as gzip_open
from os.path import exists
from pickle import dump, load

from src.engines.engine_3D.relative_paths import get_path


class VertexBufferObject:
    def __init__(self, app):
        self.app = app
        self.context = app.context
        self.vertex_buffer_objects = {
            "cube" : CubeVBO(self.context),
            "sphere" : SphereVBO(self.context),
            "skybox" : SkyboxVBO(self.context),
            "cat" : CatVBO(self.context)
        }
        if app.functions:
            for i, function in enumerate(app.functions):
                self.vertex_buffer_objects[f"surface_{i}"] = SurfaceVBO(self.context, function)

    def destroy(self):
        [vbo.destroy() for vbo in self.vertex_buffer_objects.values()]


class BaseVertexBufferObject:
    def __init__(self, context):
        self.context = context
        self.vertex_buffer_object = self.get_vertex_buffer_object()
        self.format: str=None
        self.attrib: list=None

    def get_vertex_buffer_object(self):
        return self.context.buffer(self.get_vertex_data())
    
    def destroy(self):
        self.vertex_buffer_object.release()
    
    @staticmethod
    def get_data(vertices, indices):
        return np.array([vertices[i] for triangle in indices for i in triangle], dtype="f4")


class SkyboxVBO(BaseVertexBufferObject):
    def __init__(self, context):
        super().__init__(context)
        self.format = "3f"
        self.attribs = ["in_position"]
        
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


class CubeVBO(BaseVertexBufferObject):
    def __init__(self, context):
        super().__init__(context)
        self.format = "2f 3f 3f"
        self.attribs = ["in_texcoord_0", "in_normal", "in_position"]
    
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


class External_VBO(BaseVertexBufferObject):
    def __init__(self, context):
        super().__init__(context)
        self.format = "2f 3f 3f"
        self.attribs = ["in_texcoord_0", "in_normal", "in_position"]

    def get_vertex_data(self, object_path):
        objects = Wavefront(object_path, cache=True, parse=True, create_materials=True)
        obj = objects.materials.popitem()[1]
        return np.array(obj.vertices, dtype="f4")


class SphereVBO(External_VBO):
    def get_vertex_data(self):
        return super().get_vertex_data(get_path("objects/sphere/sphere.obj"))


class CatVBO(External_VBO):
    def get_vertex_data(self):
        return super().get_vertex_data(get_path("objects/cat/20430_Cat_v1_NEW.obj"))


class SurfaceVBO(BaseVertexBufferObject):
    def __init__(self, context, function):
        self.function = function
        super().__init__(context)
        self.format = "2f 3f"
        self.attribs = ["in_texcoord_0", "in_position"]

    def get_vertex_data(self):
        # Check if the data has previously been saved
        if self.function.save_filename and exists(self.function.save_filename):
            return self.load_data()
        else:
            # Set parameters
            x_num, y_num = self.function.resolution
            x_start, x_end = self.function.x_limits
            y_start, y_end = self.function.y_limits

            # Setup array indicating the z value at every (x,y) coordinates
            x_space = np.linspace(x_start, x_end, x_num)
            y_space = np.linspace(y_start, y_end, y_num)
            x, y = np.meshgrid(x_space, y_space)
            z_array = self.function.function(x, y).T    # Transpose to format the array so the indices are given [x,y]
            # print(z_array[33,100], self.function.i)

            vertices = []       # List of every points of the screen (which will be linked together to form triangles)
            indices = []        # List of the vertices that should be connected to form triangles
            for i in range(x_num):
                for j in range(y_num):
                    current_i = i + j*x_num
                    vertices.append(((i/(x_num-1) * (x_end - x_start) + x_start), 
                                    z_array[i,j],
                                    -(j/(y_num-1) * (y_end - y_start) + y_start)))
                    if i < x_num-1 and j < y_num-1:
                        # Create first side
                        # Indices must be given in clockwise order to be viewed from the front
                        indices.append((current_i, current_i + x_num+1, current_i + x_num))
                        indices.append((current_i, current_i + 1,  current_i + x_num+1))
                        # Create other side
                        # Indices must be given in counter-clockwise order to be viewed from the front
                        indices.append((current_i, current_i + x_num, current_i + x_num+1))
                        indices.append((current_i, current_i + x_num+1, current_i + 1))


            vertex_data = self.get_data(vertices, indices)

            tex_coord_vertices = [(0,0), (1,0), (1,1), (0,1)]       # coordinates of the texture's corners

            # Texture coords vertices that should be connected to form the correct texture
            tex_coord_indices = [(0,2,3), (0,1,2), (0,3,2), (0,2,1)] * int((len(indices) / 4))
            tex_coord_data = self.get_data(tex_coord_vertices, tex_coord_indices)
            
            if self.function.save_filename:
                self.save_data(np.hstack([tex_coord_data, vertex_data]))

            return np.hstack([tex_coord_data, vertex_data])
    
    def save_data(self, array):
        with gzip_open(self.function.save_filename, "wb") as file:
            dump(array, file)

    def load_data(self) -> np.ndarray:
        with gzip_open(self.function.save_filename, "rb") as file:
            array = load(file)

        return array
    
    def update(self):
        self.vertex_buffer_object = self.get_vertex_buffer_object()
