from vertex_buffer_object import Vertex_buffer_object
from shader_program import Shader_program


class Vertex_array_object:
    def __init__(self, context):
        self.context =  context
        self.vertex_buffer_object = Vertex_buffer_object(context)
        self.program = Shader_program(context)
        self.vertex_array_objects = {
            "skybox" : self.get_vertex_array_object(
                    program=self.program.programs["skybox"],
                    vertex_buffer_object=self.vertex_buffer_object.vertex_buffer_objects["skybox"]),
            "cube" : self.get_vertex_array_object(
                    program=self.program.programs["default"],
                    vertex_buffer_object=self.vertex_buffer_object.vertex_buffer_objects["cube"]),
            "shadow_cube" : self.get_vertex_array_object(
                    program=self.program.programs["shadow_map"],
                    vertex_buffer_object=self.vertex_buffer_object.vertex_buffer_objects["cube"]),
            "sphere" : self.get_vertex_array_object(
                    program=self.program.programs["default"],
                    vertex_buffer_object=self.vertex_buffer_object.vertex_buffer_objects["sphere"]),
            "shadow_sphere" : self.get_vertex_array_object(
                    program=self.program.programs["shadow_map"],
                    vertex_buffer_object=self.vertex_buffer_object.vertex_buffer_objects["sphere"]),
            "cat" : self.get_vertex_array_object(
                    program=self.program.programs["default"],
                    vertex_buffer_object=self.vertex_buffer_object.vertex_buffer_objects["cat"]),
            "shadow_cat" : self.get_vertex_array_object(
                    program=self.program.programs["shadow_map"],
                    vertex_buffer_object=self.vertex_buffer_object.vertex_buffer_objects["cat"]),
            "surface" : self.get_vertex_array_object(
                    program=self.program.programs["surface"],
                    vertex_buffer_object=self.vertex_buffer_object.vertex_buffer_objects["surface"])
        }
        # A shadow instance must be added for every object

    def get_vertex_array_object(self, program, vertex_buffer_object):
        vbo = vertex_buffer_object
        return self.context.vertex_array(program, [(vbo.vertex_buffer_object, vbo.format, *vbo.attribs)],
                                         skip_errors=True)    # Skip errors if the VAO is not complete

    def destroy(self):
        self.vertex_buffer_object.destroy()
        self.program.destroy()
