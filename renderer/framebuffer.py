import sys
import OpenGL.GL as gl
from renderer.texture import Texture

class Framebuffer:
    def __init__(self, width, height):
        self._fbo_id = gl.glGenFramebuffers(1)
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self._fbo_id)

        self._texture = Texture(width, height)
        gl.glFramebufferTexture2D(gl.GL_FRAMEBUFFER, gl.GL_COLOR_ATTACHMENT0, gl.GL_TEXTURE_2D, self._texture.get_id(), 0)

        rbo_id = gl.glGenRenderbuffers(1)
        gl.glBindRenderbuffer(gl.GL_RENDERBUFFER, rbo_id)
        gl.glRenderbufferStorage(gl.GL_RENDERBUFFER, gl.GL_DEPTH_COMPONENT32, width, height)
        gl.glFramebufferRenderbuffer(gl.GL_FRAMEBUFFER, gl.GL_DEPTH_ATTACHMENT, gl.GL_RENDERBUFFER, rbo_id)

        if not gl.glCheckFramebufferStatus(gl.GL_FRAMEBUFFER) == gl.GL_FRAMEBUFFER_COMPLETE:
            print("Error: Framebuffer is not complete.")
            sys.exit()

        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)

    def bind(self):
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self._fbo_id)

    def unbind(self):
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)

    def get_fbo_id(self):
        return self._fbo_id
    
    def get_texture_id(self):
        return self._texture.get_id()
