import sys
import OpenGL.GL as gl

class PickingTexture:

    def __init__(self, width, height) -> None:
        self._picking_texture_id = 0
        self._fbo_id = 0
        self._depth_texture_id = 0

        if not self.init(width, height):
            print("Error: Picking texture is not complete.")
            sys.exit()

    def init(self, width, height):
        self._fbo_id = gl.glGenFramebuffers(1)
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self._fbo_id)

        self._picking_texture_id = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self._picking_texture_id)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB32F, width, height, 0, gl.GL_RGB, gl.GL_FLOAT, None)
        gl.glFramebufferTexture2D(gl.GL_FRAMEBUFFER, gl.GL_COLOR_ATTACHMENT0, gl.GL_TEXTURE_2D, self._picking_texture_id, 0)

        gl.glEnable(gl.GL_TEXTURE_2D)
        self._depth_texture_id = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self._depth_texture_id)
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_DEPTH_COMPONENT, width, height, 0, gl.GL_DEPTH_COMPONENT, gl.GL_FLOAT, None)
        gl.glFramebufferTexture2D(gl.GL_FRAMEBUFFER, gl.GL_DEPTH_ATTACHMENT, gl.GL_TEXTURE_2D, self._depth_texture_id, 0)

        gl.glReadBuffer(gl.GL_NONE)
        gl.glDrawBuffer(gl.GL_COLOR_ATTACHMENT0)

        if not gl.glCheckFramebufferStatus(gl.GL_FRAMEBUFFER) == gl.GL_FRAMEBUFFER_COMPLETE:
            print("Error: Framebuffer is not complete.")
            return False

        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)

        return True
    
    def enable_writing(self):
        gl.glBindFramebuffer(gl.GL_DRAW_FRAMEBUFFER, self._fbo_id)

    def disable_writing(self):
        gl.glBindFramebuffer(gl.GL_DRAW_FRAMEBUFFER, 0)

    def read_pixel(self, x, y):
        gl.glBindFramebuffer(gl.GL_READ_FRAMEBUFFER, self._fbo_id)
        gl.glReadBuffer(gl.GL_COLOR_ATTACHMENT0)

        pixels = gl.glReadPixels(x, y, 1.0, 1.0, gl.GL_RGB, gl.GL_FLOAT, None)

        return int(pixels[0]) - 1
