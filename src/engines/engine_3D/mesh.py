from vertex_array_object import VertexArrayObject
from texture import Texture


class Mesh:
    def __init__(self, app):
        self.app = app
        self.vertex_array_object = VertexArrayObject(app)
        self.texture = Texture(app)

    def destroy(self):
        self.vertex_array_object.destroy()
        self.texture.destroy()
