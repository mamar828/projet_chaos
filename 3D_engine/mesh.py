from vertex_array_object import Vertex_array_object
from texture import Texture


class Mesh:
    def __init__(self, app):
        self.app = app
        self.vertex_array_object = Vertex_array_object(app.context)
        self.texture = Texture(app)

    def destroy(self):
        self.vertex_array_object.destroy()
        self.texture.destroy()
