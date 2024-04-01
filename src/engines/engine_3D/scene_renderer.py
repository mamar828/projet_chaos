class SceneRenderer:
    def __init__(self, app):
        self.app = app
        self.context = app.context
        self.mesh = app.mesh
        self.scene = app.scene
        # Shadow depth buffer
        self.depth_texture = self.mesh.texture.textures["depth_texture"]
        self.depth_frame_buffer_object = self.context.framebuffer(depth_attachment=self.depth_texture)

    def render_shadow(self):
        self.depth_frame_buffer_object.clear()
        self.depth_frame_buffer_object.use()
        for obj in self.scene.objects:
            if obj.shadow_program:
                obj.render_shadow()

    def main_render(self):
        self.context.screen.use()
        if self.scene.objects:
            for obj in self.scene.objects:
                obj.render()
        if self.scene.surfaces:
            for surface in self.scene.surfaces:
                surface.render()
        self.scene.skybox.render()

    def render(self):
        # pass 1
        self.render_shadow()
        # pass 2
        self.main_render()

    def destroy(self):
        self.depth_frame_buffer_object.release()
