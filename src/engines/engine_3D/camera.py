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
            cinematic_settings: dict=None
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
        self.stable_up = glm.vec3(0,1,0)
        self.yaw = yaw
        self.pitch = pitch
        
        self.m_view = self.get_view_matrix()        # view_matrix
        self.m_proj = self.get_projection_matrix()  # projection_matrix
        self.current_speed_modifier = 1
        self.current_speed_modifier_i = 5

        self.position_mode = "free"
        self.current_tracked_body_index = -1
        self.current_tracked_body = None
        if self.app.simulation.system.tracked_bodies:
            self.body_tracking_allowed = True
        else:
            self.body_tracking_allowed = False

        self.movement_mode = None
        self.cycle_movement_modes()
        self.c_s = cinematic_settings

        # if movement_mode == "instantaneous":
        #     self.move = self.move_instaneous
        #     self.rotate = self.rotate_instantaneous

        # elif movement_mode == "cinematic":
            # self.move = self.move_cinematic
            # self.rotate = self.rotate_cinematic
            # # self.positive_acceleration_scalar = 0.05
            # self.positive_acceleration_scalar = 0.005
            # # self.negative_acceleration_scalar = 0.05
            # self.negative_acceleration_scalar = 0.0
            # # self.positive_rotation_scalar = 0.02
            # self.positive_rotation_scalar = 0.005
            # # self.negative_rotation_factor = 0.94
            # self.negative_rotation_factor = 1

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
        rotation_dict = self.app.input.get_rotation_dict()
        if rotation_dict:
            self.yaw += rotation_speed * rotation_dict["horizontal"]
            self.pitch += rotation_speed * rotation_dict["vertical"]

        self.pitch = max(-89, min(89, self.pitch))

    def move_instaneous(self):
        velocity = self.speed * self.app.camera_delta_time * self.current_speed_modifier
        movement_dict = self.app.input.get_movement_dict()
        
        if self.position_mode == "free":
            if movement_dict:
                self.position += self.forward * velocity * movement_dict["forward"]
                self.position += self.right * velocity * movement_dict["right"]
                self.position += self.up * velocity * movement_dict["up"]

        elif self.position_mode == "following":
            tracked_position = self.current_tracked_body.position
            self.set_position((tracked_position[0], tracked_position[1], self.position.y))
            if movement_dict:
                self.position += self.stable_up * velocity * movement_dict["up"]

    def rotate_cinematic(self):
        # Key controls
        rotation_speed = self.sensitivity * self.app.camera_delta_time
        rotation_dict = self.app.input.get_rotation_dict()
        if rotation_dict.get("horizontal"):
            self.rotation_vector += glm.vec2(self.c_s["positive_rotation"], 0) * rotation_dict["horizontal"]
        else:
            self.rotation_vector *=  glm.vec2(self.c_s["negative_rotation"], 1)
        
        if rotation_dict.get("vertical"):
            self.rotation_vector += glm.vec2(0, self.c_s["positive_rotation"]) * rotation_dict["vertical"]
        else:
            self.rotation_vector *=  glm.vec2(1, self.c_s["negative_rotation"])
        
        self.rotation_vector = glm.clamp(self.rotation_vector,-1,1)
        self.yaw += self.rotation_vector[0] * rotation_speed
        self.pitch += self.rotation_vector[1] * rotation_speed
        self.pitch = max(-89, min(89, self.pitch))

    def move_cinematic(self):
        velocity = self.speed * self.app.camera_delta_time * self.current_speed_modifier
        movement_dict = self.app.input.get_movement_dict()
        if self.position_mode == "free":
            if movement_dict.get("forward"):
                self.acceleration_vector += self.forward * self.c_s["positive_acceleration"] * movement_dict["forward"]
            else:
                # Apply damping
                dot_0 = glm.dot(self.acceleration_vector, self.forward)
                if dot_0 != 0:
                    self.acceleration_vector -= dot_0 / abs(dot_0) * (self.forward * self.c_s["negative_acceleration"]
                                                                      * min(1,max(-1,abs(dot_0))))

            if movement_dict.get("right"):
                self.acceleration_vector += self.right * self.c_s["positive_acceleration"] * movement_dict["right"]
            else:
                # Apply damping
                dot_1 = glm.dot(self.acceleration_vector, self.right)
                if dot_1 != 0:
                    self.acceleration_vector -= dot_1 / abs(dot_1) * (self.right * self.c_s["negative_acceleration"]
                                                                      * min(1,max(-1,abs(dot_1))))

            if movement_dict.get("up"):
                self.acceleration_vector += self.up * self.c_s["positive_acceleration"] * movement_dict["up"]
            else:
                # Apply damping
                dot_2 = glm.dot(self.acceleration_vector, self.up)
                if dot_2 != 0:
                    self.acceleration_vector -= dot_2 / abs(dot_2) * (self.up * self.c_s["negative_acceleration"]
                                                                      * min(1,max(-1,abs(dot_2))))
 
        elif self.position_mode == "following":
            tracked_position = self.current_tracked_body.position
            self.set_position((tracked_position[0], tracked_position[1], self.position.y))
            if movement_dict.get("up"):
                self.acceleration_vector +=     self.stable_up * self.c_s["positive_acceleration"] * movement_dict["up"]
            else:
                # Apply damping
                dot_2 = glm.dot(self.acceleration_vector, self.stable_up)
                if dot_2 != 0:
                    self.acceleration_vector -= dot_2 / abs(dot_2) * (self.stable_up * self.c_s["negative_acceleration"]
                                                                      * min(1,max(-1,abs(dot_2))))

        # Apply max speed
        abs_max = glm.max(glm.abs(self.acceleration_vector))
        if abs_max > 1:
            self.acceleration_vector /= abs_max
        self.position += self.acceleration_vector * velocity

    def get_view_matrix(self):
        return glm.lookAt(self.position, self.position + self.forward, self.up)

    def get_projection_matrix(self):
        return glm.perspective(glm.radians(self.FOV), self.aspect_ratio, self.NEAR, self.FAR)
    
    def cycle_tracked_bodies(self):
        if self.body_tracking_allowed:
            if self.current_tracked_body_index == len(self.app.simulation.system.tracked_bodies) - 1:
                self.current_tracked_body_index = -1
                self.position_mode = "free"
            else:
                self.current_tracked_body_index += 1
                self.current_tracked_body = self.app.simulation.system.tracked_bodies[self.current_tracked_body_index]
                self.position_mode = "following"
                self.acceleration_vector = glm.vec3(0,0,0)
                self.rotation_vector = glm.vec2(0,0)

    def cycle_movement_modes(self):
        if self.movement_mode == "instantaneous":
            self.movement_mode = "cinematic"
            self.move = self.move_cinematic
            self.rotate = self.rotate_cinematic
            # Reset previous accelerations
            self.acceleration_vector = glm.vec3(0,0,0)
            self.rotation_vector = glm.vec2(0,0)
        else:
            self.movement_mode = "instantaneous"
            self.move = self.move_instaneous
            self.rotate = self.rotate_instantaneous
