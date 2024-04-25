import glm
import pygame as pg
from numpy import array as nparray


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
            movement_mode="instantaneous"
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

        self.right = glm.vec3(1,0,0)
        self.up = glm.vec3(0,1,0)
        self.forward = glm.vec3(0,0,-1)
        self.direction_array = nparray((-self.right, self.up, self.forward))
        self.yaw = yaw
        self.pitch = pitch
        
        self.m_view = self.get_view_matrix()        # view_matrix
        self.m_proj = self.get_projection_matrix()  # projection_matrix
        self.current_speed_modifier = 1

        self.position_mode = "free"
        self.current_tracked_body_index = -1
        self.current_tracked_body = None
        if self.app.simulation.system.tracked_bodies:
            self.body_tracking_allowed = True
        else:
            self.body_tracking_allowed = False

        self.movement_mode = movement_mode

        if movement_mode == "instantaneous":
            self.move = self.move_instaneous
            self.rotate = self.rotate_instantaneous

        elif movement_mode == "cinematic":
            self.move = self.move_cinematic
            self.rotate = self.rotate_cinematic
            # self.positive_acceleration_scalar = 0.05
            self.positive_acceleration_scalar = 0.005
            # self.negative_acceleration_scalar = 0.05
            self.negative_acceleration_scalar = 0.0
            # self.positive_camera_scalar = 0.02
            self.positive_camera_scalar = 0.005
            # self.negative_camera_factor = 0.94
            self.negative_camera_factor = 1
            self.acceleration_vector = glm.vec3(0,0,0)
            self.rotation_vector = glm.vec2(0,0)

    def __str__(self):
        return f"Camera position: {self.position.x:.3f}, {-self.position.z:.3f}, {self.position.y:.3f}"
    
    def set_position(self, position: tuple):
        self.position = glm.vec3((position[0], position[2], -position[1]))

    def update_camera_vectors(self):
        yaw, pitch = glm.radians(self.yaw), glm.radians(self.pitch)

        self.forward.x = glm.cos(yaw) * glm.cos(pitch)
        self.forward.y = glm.sin(pitch)
        self.forward.z = glm.sin(yaw) * glm.cos(pitch)

        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0, 1, 0)))
        self.up = glm.normalize(glm.cross(self.right, self.forward))

    def update(self):
        self.update_states()
        self.move()
        self.rotate_mouse()
        self.rotate()
        self.update_camera_vectors()
        self.m_view = self.get_view_matrix()

    def rotate_mouse(self):
        # Mouse controls
        rel_x, rel_y = pg.mouse.get_rel()
        self.yaw += rel_x * self.sensitivity
        self.pitch -= rel_y * self.sensitivity
        self.pitch = max(-89, min(89, self.pitch))

    def rotate_instantaneous(self):
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

    def move_instaneous(self):
        velocity = self.speed * self.app.camera_delta_time * self.current_speed_modifier
        keys = pg.key.get_pressed()
        movement_array = self.app.keyboard.get_movement_array()
        
        if movement_array is not None:
            if self.position_mode == "free":
                # print(self.direction_array)
                # print(movement_array)
                # print(self.direction_array * movement_array * velocity)
                # print(*(self.direction_array * movement_array * velocity).sum(axis=0))
                vec = glm.vec3(*(self.direction_array * movement_array * velocity).sum(axis=0))
                print(vec, self.direction_array * movement_array * velocity)
                self.position += vec
        # if self.position_mode == "free":
        #     if True in list(keys):
        #         if keys[pg.K_w]:
        #             self.position += self.forward * velocity
        #         if keys[pg.K_s]:
        #             self.position -= self.forward * velocity
        #         if keys[pg.K_d]:
        #             self.position += self.right * velocity
        #         if keys[pg.K_a]:
        #             self.position -= self.right * velocity
        #         if keys[pg.K_SPACE]:
        #             self.position += self.up * velocity
        #         if keys[pg.K_LSHIFT]:
        #             self.position -= self.up * velocity

        elif self.position_mode == "following":
            tracked_position = self.current_tracked_body.position
            self.set_position((tracked_position[0], tracked_position[1], self.position.y))
            if True in list(keys):
                if keys[pg.K_SPACE]:
                    self.position += glm.vec3(0,1,0) * velocity
                if keys[pg.K_LSHIFT]:
                    self.position -= glm.vec3(0,1,0) * velocity

    def rotate_cinematic(self):
        # Key controls
        rotation_speed = self.sensitivity * self.app.camera_delta_time
        keys = pg.key.get_pressed()
        if keys[pg.K_l] or keys[pg.K_j]:
            if keys[pg.K_l]:
                self.rotation_vector += glm.vec2(self.positive_camera_scalar,0)
            if keys[pg.K_j]:
                self.rotation_vector -= glm.vec2(self.positive_camera_scalar,0)
        else:
            self.rotation_vector *= glm.vec2(self.negative_camera_factor,1)
        
        if keys[pg.K_i] or keys[pg.K_k]:
            if keys[pg.K_i]:
                self.rotation_vector += glm.vec2(0,self.positive_camera_scalar)
            if keys[pg.K_k]:
                self.rotation_vector -= glm.vec2(0,self.positive_camera_scalar)
        else:
            self.rotation_vector *= glm.vec2(1,self.negative_camera_factor)
        
        self.rotation_vector = glm.clamp(self.rotation_vector,-1,1)
        self.yaw += self.rotation_vector[0] * rotation_speed
        self.pitch += self.rotation_vector[1] * rotation_speed
        self.pitch = max(-89, min(89, self.pitch))

    def move_cinematic(self):
        velocity = self.speed * self.app.camera_delta_time * self.current_speed_modifier
        keys = pg.key.get_pressed()
        if self.position_mode == "free":
            if keys[pg.K_w] or keys[pg.K_s]:
                if keys[pg.K_w]:
                    self.acceleration_vector += self.forward * self.positive_acceleration_scalar
                elif keys[pg.K_s]:
                    self.acceleration_vector -= self.forward * self.positive_acceleration_scalar
            else:
                # Apply damping
                dot_0 = glm.dot(self.acceleration_vector, self.forward)
                if dot_0 > 0:
                    self.acceleration_vector -= self.forward * self.negative_acceleration_scalar * min(1,max(-1,abs(dot_0)))
                elif dot_0 < 0:
                    self.acceleration_vector += self.forward * self.negative_acceleration_scalar * min(1,max(-1,abs(dot_0)))

            if keys[pg.K_d] or keys[pg.K_a]:
                if keys[pg.K_d]:
                    self.acceleration_vector += self.right * self.positive_acceleration_scalar
                elif keys[pg.K_a]:
                    self.acceleration_vector -= self.right * self.positive_acceleration_scalar
            else:
                # Apply damping
                dot_1 = glm.dot(self.acceleration_vector, self.right)
                if dot_1 > 0:
                    self.acceleration_vector -= self.right * self.negative_acceleration_scalar * min(1,max(-1,abs(dot_1)))
                elif dot_1 < 0:
                    self.acceleration_vector += self.right * self.negative_acceleration_scalar * min(1,max(-1,abs(dot_1)))

            if keys[pg.K_SPACE] or keys[pg.K_LSHIFT]:
                if keys[pg.K_SPACE]:
                    self.acceleration_vector += self.up * self.positive_acceleration_scalar
                elif keys[pg.K_LSHIFT]:
                    self.acceleration_vector -= self.up * self.positive_acceleration_scalar
            else:
                # Apply damping
                dot_2 = glm.dot(self.acceleration_vector, self.up)
                if dot_2 > 0:
                    self.acceleration_vector -= self.up * self.negative_acceleration_scalar * min(1,max(-1,abs(dot_2)))
                elif dot_2 < 0:
                    self.acceleration_vector += self.up * self.negative_acceleration_scalar * min(1,max(-1,abs(dot_2)))
 
        elif self.position_mode == "following":
            tracked_position = self.current_tracked_body.position
            self.set_position((tracked_position[0], tracked_position[1], self.position.y))
            up = glm.vec3(0,1,0)
            if keys[pg.K_SPACE] or keys[pg.K_LSHIFT]:
                if keys[pg.K_SPACE]:
                    self.acceleration_vector += up * self.positive_acceleration_scalar
                elif keys[pg.K_LSHIFT]:
                    self.acceleration_vector -= up * self.positive_acceleration_scalar
            else:
                # Apply damping
                dot_2 = glm.dot(self.acceleration_vector, up)
                if dot_2 > 0:
                    self.acceleration_vector -= up * self.negative_acceleration_scalar * min(1,max(-1,abs(dot_2)))
                elif dot_2 < 0:
                    self.acceleration_vector += up * self.negative_acceleration_scalar * min(1,max(-1,abs(dot_2)))

        # Apply max speed
        abs_max = glm.max(glm.abs(self.acceleration_vector))
        if abs_max > 1:
            self.acceleration_vector /= abs_max
        self.position += self.acceleration_vector * velocity

    def get_view_matrix(self):
        return glm.lookAt(self.position, self.position + self.forward, self.up)

    def get_projection_matrix(self):
        return glm.perspective(glm.radians(self.FOV), self.aspect_ratio, self.NEAR, self.FAR)
    
    def update_states(self):
        keys = pg.key.get_pressed()
        if True in list(keys):
            if keys[pg.K_TAB] and pg.K_TAB not in self.app.pressed_keys and self.body_tracking_allowed:
                self.app.pressed_keys.add(pg.K_TAB)
                if self.current_tracked_body_index == len(self.app.simulation.system.tracked_bodies) - 1:
                    self.current_tracked_body_index = -1
                    self.position_mode = "free"
                else:
                    self.current_tracked_body_index += 1
                    self.current_tracked_body = self.app.simulation.system.tracked_bodies[
                                                                                        self.current_tracked_body_index]
                    self.position_mode = "following"

            if self.app.key_mode == "camera":
                for i in range(1,10):
                    if keys[getattr(pg, f"K_{i}")]:
                        if i <= 5:
                            self.current_speed_modifier = 1 / 5**3 * i**3
                        else:
                            self.current_speed_modifier = 1 / 5**6 * i**6
                        break
