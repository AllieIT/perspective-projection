import itertools
import numpy as np
import pygame as pg
from camera import Camera
from game_math import Vector3, Vector2

WIDTH, HEIGHT = 1280, 720

COLORS = {
    "WHITE": (255, 255, 255),
    "RED": (255, 0, 0),
    "BLUE": (0, 0, 255),
    "BLACK": (0, 0, 0),
}


def initialize_cube():
    cube_point_coords = [-1, 1]
    coords = list(itertools.product(cube_point_coords, cube_point_coords, cube_point_coords))
    points_to_project = [np.array(product).transpose() for product in coords]
    vector3_points = [Vector3(point[0], point[1], point[2]) for point in points_to_project]

    return vector3_points


def init():
    pg.init()
    pg.display.set_caption("3D Projection")
    cam = Camera(Vector3(0, 0, 0), 5, Vector2(1280, 720))
    display = pg.display.set_mode((cam.resolution.x, cam.resolution.y))
    main_loop(display, initialize_cube(), cam)
    print("Hello")


def draw_line(display, positions):
    pos_1 = (positions[0].x, positions[0].y)
    pos_2 = (positions[1].x, positions[1].y)
    # if pos_1[0] < 0 or pos_1[1] < 0 or pos_2[0] < 0 or pos_2[1] < 0:
    #     return
    pg.draw.aaline(display, COLORS["BLACK"], pos_1, pos_2, 2)


def draw_point(display, vector2_position, size):
    position = (vector2_position.x, vector2_position.y)
    pg.draw.circle(display, COLORS["BLACK"], position, size)


def main_loop(display, points, cam):
    running = True
    fps = 60
    clock = pg.time.Clock()
    cam_rotation_speed = 0.01

    cam_debug = Camera(Vector3(0, 0, 0), 5, Vector2(1280, 720))

    points_to_connect = [
        [0, 1], [0, 2], [1, 3], [2, 3],
        [4, 5], [4, 6], [5, 7], [6, 7],
        [0, 4], [1, 5], [2, 6], [3, 7]
    ]

    while running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    running = False

        keys = pg.key.get_pressed()

        if keys[pg.K_LSHIFT]:
            cam_rotation_speed = 0.03
        if not keys[pg.K_LSHIFT]:
            cam_rotation_speed = 0.01
        if keys[pg.K_RIGHT]:
            cam.rotation_angles = (cam.rotation_angles[0] - cam_rotation_speed, cam.rotation_angles[1])
        if keys[pg.K_LEFT]:
            cam.rotation_angles = (cam.rotation_angles[0] + cam_rotation_speed, cam.rotation_angles[1])
        if keys[pg.K_UP]:
            cam.rotation_angles = (cam.rotation_angles[0], cam.rotation_angles[1] + cam_rotation_speed)
        if keys[pg.K_DOWN]:
            cam.rotation_angles = (cam.rotation_angles[0], cam.rotation_angles[1] - cam_rotation_speed)
        if keys[pg.K_q]:
            cam.plane_scale += 0.01
        if keys[pg.K_e]:
            if cam.plane_scale > 0.1:
                cam.plane_scale -= 0.01
        if keys[pg.K_o]:
            cam.look_distance += 0.1
        if keys[pg.K_p]:
            if cam.look_distance > 1:
                cam.look_distance -= 0.1
        # if keys[pg.K_w]:
        #     cam.look_position = cam.look_position.add(Vector3(0.01, 0, 0))
        # if keys[pg.K_s]:
        #     cam.look_position = cam.look_position.add(Vector3(-0.01, 0, 0))
        # if keys[pg.K_a]:
        #     cam.look_position = cam.look_position.add(Vector3(0, 0, -0.01))
        # if keys[pg.K_d]:
        #     cam.look_position = cam.look_position.add(Vector3(0, 0, 0.01))
        # if keys[pg.K_SPACE]:
        #     cam.look_position = cam.look_position.add(Vector3(0, 0.01, 0))
        # if keys[pg.K_LSHIFT]:
        #     cam.look_position = cam.look_position.add(Vector3(0, -0.01, 0))

        cam.recalculate()
        display.fill(COLORS["WHITE"])

        camera_points = [cam.get_point_position(point) for point in points]
        camera_sizes = [cam.get_size(point) for point in points]

        for i, point in enumerate(camera_points):
            draw_point(display, point, camera_sizes[i])

        for position_index in points_to_connect:
            draw_line(display, (camera_points[position_index[0]], camera_points[position_index[1]]))

        pg.display.flip()
        clock.tick(fps)

    pg.quit()
    exit()


init()