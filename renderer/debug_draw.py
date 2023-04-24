import ctypes
from math import sin, cos, radians
import glm
import numpy as np
import OpenGL.GL as gl

from renderer.line_2d import Line2D
from utils.asset_pool import AssetPool


def rotate(point, angle, origin):
    translated_point = glm.sub(point, origin)
    new_x = translated_point.x * cos(radians(angle)) - translated_point.y * sin(
        radians(angle)
    )
    new_y = translated_point.x * sin(radians(angle)) + translated_point.y * cos(
        radians(angle)
    )
    return glm.add(glm.fvec2(new_x, new_y), origin)


class DebugDraw:
    _MAX_LINES = 3000

    _lines = []
    _vertex_array = np.zeros(_MAX_LINES * 6 * 2, dtype=np.float32)

    _vao_id, _vbo_id = 0, 0

    _started = False

    @classmethod
    def start(cls):
        cls._shader = AssetPool.get_shader("assets/shaders", "debug_line_2d")
        cls._vao_id = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(cls._vao_id)

        cls._vbo_id = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, cls._vbo_id)
        gl.glBufferData(
            gl.GL_ARRAY_BUFFER,
            cls._vertex_array.nbytes,
            cls._vertex_array,
            gl.GL_DYNAMIC_DRAW,
        )

        gl.glVertexAttribPointer(
            0, 3, gl.GL_FLOAT, False, 6 * np.float32(1).nbytes, None
        )
        gl.glEnableVertexAttribArray(0)

        gl.glVertexAttribPointer(
            1,
            3,
            gl.GL_FLOAT,
            False,
            6 * np.float32(1).nbytes,
            ctypes.c_void_p(3 * np.float32(1).nbytes),
        )
        gl.glEnableVertexAttribArray(1)

        gl.glLineWidth(2.0)

    @classmethod
    def begin_frame(cls):
        if not cls._started:
            cls.start()
            cls._started = True

        cls._lines[:] = [line for line in cls._lines if line.begin_frame() > 0]

    @classmethod
    def draw(cls):
        from metroid_maker.window import Window

        if len(cls._lines) <= 0:
            return

        index = 0
        for line in cls._lines:
            for i in range(2):
                position = None

                if i == 0:
                    position = line.get_start()
                else:
                    position = line.get_end()

                color = line.get_color()

                cls._vertex_array[index] = position.x
                cls._vertex_array[index + 1] = position.y
                cls._vertex_array[index + 2] = -10.0

                cls._vertex_array[index + 3] = color.x
                cls._vertex_array[index + 4] = color.y
                cls._vertex_array[index + 5] = color.z
                index += 6

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, cls._vbo_id)
        gl.glBufferSubData(
            gl.GL_ARRAY_BUFFER,
            0,
            len(cls._vertex_array[0 : len(cls._lines) * 6 * 2]) * np.float32(1).nbytes,
            cls._vertex_array[0 : len(cls._lines) * 6 * 2],
        )

        cls._shader.use()
        cls._shader.upload_fmat4(
            "uProjection", Window.get_scene().camera().get_projection_matrix()
        )
        cls._shader.upload_fmat4("uView", Window.get_scene().camera().get_view_matrix())

        gl.glBindVertexArray(cls._vao_id)
        gl.glEnableVertexAttribArray(0)
        gl.glEnableVertexAttribArray(1)

        gl.glDrawArrays(gl.GL_LINES, 0, len(cls._lines) * 6 * 2)

        gl.glDisableVertexAttribArray(0)
        gl.glDisableVertexAttribArray(1)

        cls._shader.detach()

    @classmethod
    def add_line_2d(cls, start, end, color=glm.fvec3(0.0, 1.0, 0.0), lifetime=2):
        from metroid_maker.window import Window

        camera = Window.get_scene().camera()
        camera_left = glm.add(camera._position, glm.fvec2(-2.0, -2.0))
        camera_right = glm.add(
            glm.add(
                camera.get_projection_size(),
                glm.mul(camera.get_projection_size(), camera.get_zoom()),
            ),
            glm.fvec2(4.0, 4.0),
        )
        line_in_view = (
            (start.x >= camera_left.x and start.x <= camera_right.x)
            and (start.y >= camera_left.y and start.y <= camera_right.y)
        ) or (
            (end.x >= camera_left.x and end.x <= camera_right.x)
            and (end.y >= camera_left.y and end.y <= camera_right.y)
        )
        if len(cls._lines) >= cls._MAX_LINES or not line_in_view:
            return
        cls._lines.append(Line2D(start, end, color, lifetime))

    @classmethod
    def add_box_2d(
        cls, center, dimensions, rotation, color=glm.fvec3(0.0, 1.0, 0.0), lifetime=2
    ):
        min_vertex = glm.sub(center, glm.mul(dimensions, 0.5))
        max_vertex = glm.add(center, glm.mul(dimensions, 0.5))

        vertices = [
            glm.fvec2(min_vertex.x, min_vertex.y),
            glm.fvec2(min_vertex.x, max_vertex.y),
            glm.fvec2(max_vertex.x, max_vertex.y),
            glm.fvec2(max_vertex.x, min_vertex.y),
        ]

        if rotation != 0.0:
            vertices[:] = [rotate(vertex, rotation, center) for vertex in vertices]

        cls.add_line_2d(vertices[0], vertices[1], color, lifetime)
        cls.add_line_2d(vertices[0], vertices[3], color, lifetime)
        cls.add_line_2d(vertices[1], vertices[2], color, lifetime)
        cls.add_line_2d(vertices[2], vertices[3], color, lifetime)

    @classmethod
    def add_circle(cls, center, radius, color=glm.fvec3(0.0, 1.0, 0.0), lifetime=2):
        num_points = 20
        increment = int(360 // num_points)
        points = [
            glm.add(rotate(glm.fvec2(radius, 0.0), increment * i, glm.fvec2()), center)
            for i in range(num_points)
        ]

        for i, point in enumerate(points):
            cls.add_line_2d(points[i - 1], point, color, lifetime)
