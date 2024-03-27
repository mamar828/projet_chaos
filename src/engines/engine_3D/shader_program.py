from src.engines.engine_3D.relative_paths import get_path


class ShaderProgram:
    def __init__(self, context):
        self.context =  context
        self.programs = {
            "default" : self.get_program("default"),
            "skybox" : self.get_program("skybox"),
            "shadow_map" : self.get_program("shadow_map"),
            "surface" : self.get_program("surface")
        }

    def get_program(self, shader_program_name):
        with open(get_path(f"shaders/{shader_program_name}.vert")) as file:
            vertex_shader = file.read()

        with open(get_path(f"shaders/{shader_program_name}.frag")) as file:
            fragment_shader = file.read()

        return self.context.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        
    def destroy(self):
        [program.release() for program in self.programs.values()]
