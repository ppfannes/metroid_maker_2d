import ctypes
import glm
import numpy as np
import OpenGL.GL as gl

from renderer.line_2d import Line2D
from utils.asset_pool import AssetPool

class DebugDraw:

    _MAX_LINES = 500

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
        gl.glBufferData(gl.GL_ARRAY_BUFFER, cls._vertex_array.nbytes, cls._vertex_array, gl.GL_DYNAMIC_DRAW)

        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, False, 6 * np.float32(1).nbytes, None)
        gl.glEnableVertexAttribArray(0)

        gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, False, 6 * np.float32(1).nbytes, ctypes.c_void_p(3 * np.float32(1).nbytes))
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
        gl.glBufferSubData(gl.GL_ARRAY_BUFFER, 0, len(cls._vertex_array[0:len(cls._lines) * 6 * 2]) * np.float32(1).nbytes, cls._vertex_array[0:len(cls._lines) * 6 * 2])

        cls._shader.use()
        cls._shader.upload_fmat4("uProjection", Window.get_scene().camera().get_projection_matrix())
        cls._shader.upload_fmat4("uView", Window.get_scene().camera().get_view_matrix())

        gl.glBindVertexArray(cls._vao_id)
        gl.glEnableVertexAttribArray(0)
        gl.glEnableVertexAttribArray(1)

        gl.glDrawArrays(gl.GL_LINES, 0, len(cls._lines) * 6 * 2)

        gl.glDisableVertexAttribArray(0)
        gl.glDisableVertexAttribArray(1)

        cls._shader.detach()

    @classmethod
    def add_line_2d(cls, start, end, color=glm.fvec3(0.0, 1.0, 0.0), lifetime=1):
        if len(cls._lines) >= cls._MAX_LINES:
            return
        cls._lines.append(Line2D(start, end, color, lifetime))
