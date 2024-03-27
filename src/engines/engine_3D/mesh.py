from src.engines.engine_3D.vertex_array_object import VertexArrayObject
from src.engines.engine_3D.texture import Texture


class Mesh:
    def __init__(self, app):
        self.app = app
        self.vertex_array_object = VertexArrayObject(app)
        self.texture = Texture(app)

    def destroy(self):
        self.vertex_array_object.destroy()
        self.texture.destroy()
