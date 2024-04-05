import glm
import pygame as pg


class Camera:
    def __init__(
            self,
            app,
            position=(0,0,0),
            speed=0.025,
            sensitivity=0.1,
            fov=50,
            near_render_distance=0.1,
            far_render_distance=1000,
            yaw=-90,
            pitch=0,
            movement_mode="free",
            rotation_mode="instantaneous"
        ):
        self.app = app
        self.speed = speed
        self.sensitivity = sensitivity
        self.FOV = fov
        self.NEAR = near_render_distance
        self.FAR = far_render_distance
        self.aspect_ratio = app.window_size[0] / app.window_size[1]
        self.position = None
        self.set_position(position)
        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1,0,0)
        self.forward = glm.vec3(0,0,-1)
        self.yaw = yaw
        self.pitch = pitch
        self.m_view = self.get_view_matrix()        # view_matrix
        self.m_proj = self.get_projection_matrix()  # projection_matrix
        self.current_speed_modifier = 1
        self.movement_mode = movement_mode
        self.rotation_mode = rotation_mode
        

    def __str__(self):
        return f"Camera position: {self.position.x:.3f}, {-self.position.z:.3f}, {self.position.y:.3f}"
    
    def set_position(self, position: tuple):
        self.position = glm.vec3((position[0], position[2], -position[1]))

    def rotate(self):
        # Mouse controls
        rel_x, rel_y = pg.mouse.get_rel()
        self.yaw += rel_x * self.sensitivity
        self.pitch -= rel_y * self.sensitivity

        # Key controls
        rotation_speed = self.sensitivity * self.app.camera_delta_time
        keys = pg.key.get_pressed()
        if keys[pg.K_l]:
            self.yaw += rotation_speed
        if keys[pg.K_j]:
            self.yaw -= rotation_speed
        if keys[pg.K_i]:
            self.pitch += rotation_speed
        if keys[pg.K_k]:
            self.pitch -= rotation_speed
        
        self.pitch = max(-89, min(89, self.pitch))

    def update_camera_vectors(self):
        yaw, pitch = glm.radians(self.yaw), glm.radians(self.pitch)

        self.forward.x = glm.cos(yaw) * glm.cos(pitch)
        self.forward.y = glm.sin(pitch)
        self.forward.z = glm.sin(yaw) * glm.cos(pitch)

        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0, 1, 0)))
        self.up = glm.normalize(glm.cross(self.right, self.forward))

    def update(self):
        self.update_speed_modifier()
        self.move()
        self.rotate()
        self.update_camera_vectors()
        self.m_view = self.get_view_matrix()

    def move(self):
        velocity = self.speed * self.app.camera_delta_time * self.current_speed_modifier
        keys = pg.key.get_pressed()
        if self.movement_mode == "free":
            if True in list(keys):
                if keys[pg.K_w]:
                    self.position += self.forward * velocity
                if keys[pg.K_s]:
                    self.position -= self.forward * velocity
                if keys[pg.K_a]:
                    self.position -= self.right * velocity
                if keys[pg.K_d]:
                    self.position += self.right * velocity
                if keys[pg.K_SPACE]:
                    self.position += self.up * velocity
                if keys[pg.K_LSHIFT]:
                    self.position -= self.up * velocity

        elif self.movement_mode == "following":
            tracked_position = self.app.simulation.system.tracked_body.position
            self.set_position((tracked_position[0], tracked_position[1], self.position.y))
            if True in list(keys):
                if keys[pg.K_SPACE]:
                    self.position += glm.vec3(0,1,0) * velocity
                if keys[pg.K_LSHIFT]:
                    self.position -= glm.vec3(0,1,0) * velocity

    def get_view_matrix(self):
        return glm.lookAt(self.position, self.position + self.forward, self.up)
        # return glm.lookAt(self.position, glm.vec3(0), self.up) # Camera centered on the origin looking at point (0,0)

    def get_projection_matrix(self):
        return glm.perspective(glm.radians(self.FOV), self.aspect_ratio, self.NEAR, self.FAR)
    
    def update_speed_modifier(self):
        if self.app.key_mode == "camera":
            keys = pg.key.get_pressed()
            if True in list(keys):
                for i in range(1,10):
                    if keys[getattr(pg, f"K_{i}")]:
                        if i <= 5:
                            self.current_speed_modifier = 1 / 5**3 * i**3
                        else:
                            self.current_speed_modifier = 1 / 5**6 * i**6
                        break
