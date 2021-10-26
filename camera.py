from math import *
from game_math import Vector2, Vector3, Plane, Line
import numpy as np


class Camera:
    clipping_planes = [0, 100]
    plane_distance = 20
    plane_scale = 1 / 3
    euler_angles = []
    central_point_on_plane = None
    plane = None
    top_left_corner = None
    horizontal_vector = None
    vertical_vector = None
    plane_corners = None

    def __init__(self, look_position, look_distance, resolution):
        self.look_distance = look_distance
        self.look_position = look_position
        self.rotation_angles = (pi / 16, pi / 4)
        self.resolution = resolution
        self.aspect_ratio = resolution.x / resolution.y

        self.position = Vector3(self.look_distance * cos(self.rotation_angles[1]) * cos(self.rotation_angles[0]),
                                self.look_distance * sin(self.rotation_angles[1]),
                                self.look_distance * cos(self.rotation_angles[1]) * sin(self.rotation_angles[0]))

        self.plane_size = Vector2(self.plane_scale * self.plane_distance * self.aspect_ratio,
                                  self.plane_scale * self.plane_distance)
        print(self.plane_size)
        self.normalVector = self.position - self.look_position
        self.get_plane_equation()

    def get_plane_equation(self):
        vector_len = self.normalVector.get_magnitude()
        vector_to_plane = self.normalVector * (self.plane_distance / vector_len)
        self.central_point_on_plane = self.position - vector_to_plane

        plane_c = self.normalVector.x * self.central_point_on_plane.x + self.normalVector.y * self.central_point_on_plane.y + self.normalVector.z * self.central_point_on_plane.z

        self.plane = Plane(self.normalVector.x,
                           self.normalVector.y,
                           self.normalVector.z,
                           plane_c)

        self.get_plane_corners()
        self.get_point_position(Vector3(0, 0, 0))

    def get_plane_corners(self):

        vector_vertical = Vector3(- self.plane_size.y * sin(self.rotation_angles[1]) * cos(self.rotation_angles[0]),
                                  self.plane_size.y * cos(self.rotation_angles[1]),
                                  - self.plane_size.y * sin(self.rotation_angles[1]) * sin(self.rotation_angles[0]))

        vector_horizontal = Vector3(self.plane_size.x * sin(self.rotation_angles[0]),
                                    0,
                                    self.plane_size.x * cos(self.rotation_angles[0]))

        self.plane_corners = [self.central_point_on_plane + vector_vertical + vector_horizontal,  # Top Right
                              self.central_point_on_plane + vector_vertical - vector_horizontal,  # Top Left
                              self.central_point_on_plane - vector_vertical + vector_horizontal,  # Bottom Right
                              self.central_point_on_plane - vector_vertical - vector_horizontal]  # Bottom Left

        self.top_left_corner = self.plane_corners[1]
        self.vertical_vector = vector_vertical * -2
        self.horizontal_vector = vector_horizontal * 2

    def get_point_position(self, point):
        line_through_points = Line(self.position, point)
        intersection = self.plane.get_intersection(line_through_points)
        if intersection:
            vector_from_top_left = intersection - self.top_left_corner

            if self.horizontal_vector.x == self.horizontal_vector.y == 0:
                W = np.matrix([
                    [self.horizontal_vector.x, self.vertical_vector.x],
                    [self.horizontal_vector.z, self.vertical_vector.z]
                ])

                W_a = np.matrix([
                    [vector_from_top_left.x, self.vertical_vector.x],
                    [vector_from_top_left.z, self.vertical_vector.z]
                ])

                W_b = np.matrix([
                    [self.horizontal_vector.x, vector_from_top_left.x],
                    [self.horizontal_vector.z, vector_from_top_left.z]
                ])

            else:
                W = np.matrix([[self.horizontal_vector.x, self.vertical_vector.x],
                               [self.horizontal_vector.y, self.vertical_vector.y]])
                W_a = np.matrix([[vector_from_top_left.x, self.vertical_vector.x],
                                 [vector_from_top_left.y, self.vertical_vector.y]])
                W_b = np.matrix([[self.horizontal_vector.x, vector_from_top_left.x],
                                 [self.horizontal_vector.y, vector_from_top_left.y]])

            W_det = np.linalg.det(W)
            W_a_det = np.linalg.det(W_a)
            W_b_det = np.linalg.det(W_b)

            a = W_a_det / W_det
            b = W_b_det / W_det

            position = Vector2(round(self.resolution.x * a), round(self.resolution.y * b))
            return position

    def recalculate(self):

        self.position = Vector3(self.look_distance * cos(self.rotation_angles[1]) * cos(self.rotation_angles[0]),
                                self.look_distance * sin(self.rotation_angles[1]),
                                self.look_distance * cos(self.rotation_angles[1]) * sin(self.rotation_angles[0]))

        self.plane_size = Vector2(self.plane_scale * self.plane_distance * self.aspect_ratio,
                                  self.plane_scale * self.plane_distance)

        self.normalVector = self.position - self.look_position
        self.get_plane_equation()

    def get_size(self, point):
        distance = (self.position - point).get_magnitude()
        return 10 / distance / self.plane_scale
