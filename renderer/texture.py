from PIL import Image
import OpenGL.GL as gl

class Texture:

    def __init__(self, width=0, height=0):
        if width == 0 or height == 0:
            self._tex_id = -1
            self._width = -1
            self._height = -1
            return

        self._file_path = "Generated"

        self._tex_id = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self._tex_id)

        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)

        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB, width, height, 0, gl.GL_RGB, gl.GL_UNSIGNED_BYTE, None)

    def init(self, file_path: str):
        self._file_path = file_path

        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

        self._tex_id = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self._tex_id)

        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)

        image = Image.open(file_path).convert("RGBA").transpose(Image.FLIP_TOP_BOTTOM)

        self._width = image.width
        self._height = image.height

        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, image.width, image.height, 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, image.tobytes())

        image.close()

        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)

    def bind(self):
        gl.glBindTexture(gl.GL_TEXTURE_2D, self._tex_id)

    def unbind(self):
        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height
    
    def get_id(self):
        return self._tex_id
    
    def get_file_path(self):
        return self._file_path
    
    def __getstate__(self):
        state = self.__dict__.copy()
        del state['_tex_id']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self._tex_id = 0
