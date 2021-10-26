from math import *


class Vector2:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_magnitude(self):
        return sqrt(self.x ** 2 + self.y **2)

    def as_tuple(self):
        return self.x, self.y

    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'

    def __add__(self, v):
        return Vector2(self.x + v.x, self.y + v.y)

    def __sub__(self, v):
        return Vector2(self.x - v.x, self.y - v.y)

    def __mul__(self, value):
        try:
            return Vector2(self.x * value, self.y * value)
        except TypeError:
            return self

    def __truediv__(self, value):
        try:
            return Vector2(self.x / value, self.y / value)
        except TypeError:
            return self


class Vector3:

    def __init__(self, x, y ,z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, vector):
        return Vector3(self.x + vector.x, self.y + vector.y, self.z + vector.z)

    def __sub__(self, vector):
        return Vector3(self.x - vector.x, self.y - vector.y, self.z - vector.z)

    def __mul__(self, value):
        return Vector3(self.x * value, self.y * value, self.z * value)

    def get_magnitude(self):
        return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ', ' + str(self.z) + ')'


class Plane:

    def __init__(self, x, y, z, c):
        self.x = x
        self.y = y
        self.z = z
        self.c = c

    def __str__(self):
        return str(self.x) + 'x + ' + str(self.y) + 'y + ' + str(self.z) + 'z = ' + str(self.c)

    def get_intersection(self, line):

        if line.x.x * self.x + line.y.x * self.y + line.z.x * self.z == 0:
            return None

        t = - (self.x * line.x.y + self.y * line.y.y + self.z * line.z.y - self.c) / (line.x.x * self.x + line.y.x * self.y + line.z.x * self.z)
        intersection = Vector3(line.x.x * t + line.x.y, line.y.x * t + line.y.y, line.z.x * t + line.z.y)
        return intersection


class Line:

    def __init__(self, point_1, point_2):
        self.x = Vector2(point_2.x - point_1.x, point_1.x)      # x of Vector is t coefficient
        self.y = Vector2(point_2.y - point_1.y, point_1.y)
        self.z = Vector2(point_2.z - point_1.z, point_1.z)

    def __str__(self):
        return 'x = ' + str(self.x.y) + ' + ' + str(self.x.x) + 't\n' + 'y = ' + str(self.y.y) + ' + ' + str(self.y.x) + 't\n' + 'z = ' + str(self.z.y) + ' + ' + str(self.z.x) + 't'

