from relative_paths import get_path


class Shader_program:
    def __init__(self, context):
        self.context =  context
        self.programs = {
            "default" : self.get_program("default"),
            "skybox" : self.get_program("skybox"),
            "shadow_map" : self.get_program("shadow_map"),
            "surface" : self.get_program("surface")
        }

    def get_program(self, shader_program_name, extensions: tuple[str,str]=("vert", "frag")):
        with open(get_path(f"shaders/{shader_program_name}.{extensions[0]}")) as file:
            vertex_shader = file.read()

        # if shader_program_name.startswith("surface"): shader_program_name = "surface/fragment"
        
        with open(get_path(f"shaders/{shader_program_name}.{extensions[1]}")) as file:
            fragment_shader = file.read()

        return self.context.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        
    def destroy(self):
        [program.release() for program in self.programs.values()]
