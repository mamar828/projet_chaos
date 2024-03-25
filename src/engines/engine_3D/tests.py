import numpy as np
import pygame as pg
from relative_paths import get_path

a = np.array([1,2,3])
b = np.array([4,5,6])
c = np.array([7,8,9])


# print(np.hstack([a,b,c]))



class Planet:
    def __init__(self, position):
        self.x_position, self.y_position, self.z_position = position
        self.direction = 1

    def update(self, delta_time):
        """Update the planet's position by its speed multiplied by time"""
        if self.z_position > 50:
            self.direction *= -1
        if self.z_position < -50:
            self.direction *= -1
        self.z_position += 0.01 * delta_time * self.direction

    def get_position(self):
        return self.x_position, self.y_position, self.z_position


class Floor:
    def __init__(self, position):
        self.x_position, self.y_position, self.z_position = position

    def update(self, delta_time):
        """Update the planet's position by its speed multiplied by time"""
        pass

    def get_position(self):
        return self.x_position, self.y_position, self.z_position



class Mode7:
    def __init__(self, app):
        self.app = app
        self.floor_tex = pg.image.load(get_path("textures/floor_test.png")).convert()
        self.tex_size = self.floor_tex.get_size()
        self.floor_array = pg.surfarray.array3d(self.floor_tex)

        self.screen_array = pg.surfarray.array3d(pg.Surface(app.window_size))

        # self.alt = 1.0
        # self.angle = 0.0
        # self.pos = np.array([0.0, 0.0])

    def update(self):
        # self.movement()
        # self.screen_array = self.render_frame(self.floor_array, self.ceil_array, self.screen_array,
        #                                       self.tex_size, self.angle, self.pos, self.alt)
        self.screen_array = self.render_frame()

    def draw(self):
        pg.surfarray.blit_array(self.app.screen, self.screen_array)

    # @staticmethod
    # @njit(fastmath=True, parallel=True)
    def render_frame(self):
        # iterating over the screen array
        for i in range(self.app.window_size[0]):
            for j in range(self.app.window_size[1]):
                x = self.app.window_size[0]/2 - i
                FOCAL_LEN = 250
                SCALE = 100
                y = j + FOCAL_LEN
                z = j + 0.01

                # rotation
                px = x / z * SCALE
                py = y / z * SCALE

                # floor projection and transformation
                # floor_x = px / z - player_pos[1]
                # floor_y = py / z + player_pos[0]

                # floor pos and color
                floor_pos = int(px % self.tex_size[0]), int(py % self.tex_size[1])
                floor_col = self.floor_array[floor_pos]

                # ceil projection and transformation
                # ceil_x = alt * px / z - player_pos[1] * 0.3
                # ceil_y = alt * py / z + player_pos[0] * 0.3

                # # ceil pos and color
                # ceil_pos = int(ceil_x * SCALE % tex_size[0]), int(ceil_y * SCALE % tex_size[1])
                # ceil_col = ceil_array[ceil_pos]

                # # shading
                # # depth = 4 * abs(z) / HALF_HEIGHT
                # depth = min(max(2.5 * (abs(z) / HALF_HEIGHT), 0), 1)
                # fog = (1 - depth) * 230

                # floor_col = (floor_col[0] * depth + fog,
                #              floor_col[1] * depth + fog,
                #              floor_col[2] * depth + fog)

                # ceil_col = (ceil_col[0] * depth + fog,
                #             ceil_col[1] * depth + fog,
                #             ceil_col[2] * depth + fog)

                # # fill screen array
                self.screen_array[i, j] = floor_col
                # screen_array[i, -j] = ceil_col

                # next depth
                # new_alt += alt

        return self.screen_array

    # def movement(self):
    #     sin_a = np.sin(self.angle)
    #     cos_a = np.cos(self.angle)
    #     dx, dy = 0, 0
    #     speed_sin = SPEED * sin_a
    #     speed_cos = SPEED * cos_a

    #     keys = pg.key.get_pressed()
    #     if keys[pg.K_w]:
    #         dx += speed_cos
    #         dy += speed_sin
    #     if keys[pg.K_s]:
    #         dx += -speed_cos
    #         dy += -speed_sin
    #     if keys[pg.K_a]:
    #         dx += speed_sin
    #         dy += -speed_cos
    #     if keys[pg.K_d]:
    #         dx += -speed_sin
    #         dy += speed_cos
    #     self.pos[0] += dx
    #     self.pos[1] += dy

    #     if keys[pg.K_LEFT]:
    #         self.angle -= SPEED
    #     if keys[pg.K_RIGHT]:
    #         self.angle += SPEED

    #     if keys[pg.K_q]:
    #         self.alt += SPEED
    #     if keys[pg.K_e]:
    #         self.alt -= SPEED
    #     self.alt = min(max(self.alt, 0.3), 4.0)