import ctypes
from functools import total_ordering
import numpy as np
import OpenGL.GL as gl

from components.sprite_renderer import SpriteRenderer
from utils.asset_pool import AssetPool

@total_ordering
class RenderBatch:
    def __init__(self, max_batch_size: int, z_index: int) -> None:
        self._POS_SIZE = 2
        self._COLOR_SIZE = 4
        self._TEX_COORDS_SIZE = 2
        self._TEX_ID_SIZE = 1

        self._POS_OFFSET = 0
        self._COLOR_OFFSET = self._POS_OFFSET + self._POS_SIZE * np.float32(1).nbytes
        self._TEX_COORDS_OFFSET = self._COLOR_OFFSET + self._COLOR_SIZE * np.float32(1).nbytes
        self._TEX_ID_OFFSET = self._TEX_COORDS_OFFSET + self._TEX_COORDS_SIZE * np.float32(1).nbytes
        self._VERTEX_SIZE = 9
        self._VERTEX_SIZE_BYTES = self._VERTEX_SIZE * np.float32(1).nbytes

        self._vao_id, self._vbo_id = 0, 0

        self._shader = AssetPool.get_shader("assets/shaders", "default")
        self._sprites = [None for _ in range(max_batch_size)]
        self._textures = []
        self._tex_slots = np.array(list(range(8)), dtype=np.int32)
        self._max_batch_size = max_batch_size
        self._z_index = z_index

        self._vertices = np.zeros(max_batch_size * 4 * self._VERTEX_SIZE, dtype=np.float32)
        
        self._num_sprites = 0
        self._has_room = True
        self._texture_ids = [gl.GL_TEXTURE0, gl.GL_TEXTURE1, gl.GL_TEXTURE2, gl.GL_TEXTURE3, gl.GL_TEXTURE4, gl.GL_TEXTURE5, gl.GL_TEXTURE6, gl.GL_TEXTURE7, gl.GL_TEXTURE8]

    def __lt__(self, other: 'RenderBatch'):
        return self._z_index < other._z_index
        
    def start(self):
        self._vao_id = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self._vao_id)

        self._vbo_id = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self._vbo_id)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, self._vertices.size * np.float32(1).nbytes, self._vertices, gl.GL_DYNAMIC_DRAW)

        ebo_id = gl.glGenBuffers(1)
        indices = self._generate_indices()
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, ebo_id)
        gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, indices.size * np.float32(1).nbytes, indices, gl.GL_STATIC_DRAW)

        gl.glVertexAttribPointer(0, self._POS_SIZE, gl.GL_FLOAT, False, self._VERTEX_SIZE_BYTES, ctypes.c_void_p(self._POS_OFFSET))
        gl.glEnableVertexAttribArray(0)

        gl.glVertexAttribPointer(1, self._COLOR_SIZE, gl.GL_FLOAT, False, self._VERTEX_SIZE_BYTES, ctypes.c_void_p(self._COLOR_OFFSET))
        gl.glEnableVertexAttribArray(1)

        gl.glVertexAttribPointer(2, self._TEX_COORDS_SIZE, gl.GL_FLOAT, False, self._VERTEX_SIZE_BYTES, ctypes.c_void_p(self._TEX_COORDS_OFFSET))
        gl.glEnableVertexAttribArray(2)

        gl.glVertexAttribPointer(3, self._TEX_ID_SIZE, gl.GL_FLOAT, False, self._VERTEX_SIZE_BYTES, ctypes.c_void_p(self._TEX_ID_OFFSET))
        gl.glEnableVertexAttribArray(3)

    def add_sprite(self, sprite_renderer: SpriteRenderer):
        index = self._num_sprites
        self._sprites[index] = sprite_renderer
        self._num_sprites += 1

        if sprite_renderer.get_texture() is not None:
            if not sprite_renderer.get_texture() in self._textures:
                self._textures.append(sprite_renderer.get_texture())

        self._load_vertex_properties(index)

        if self._num_sprites >= self._max_batch_size:
            self._has_room = False

    def render(self, camera):
        rebuffer_data = False
        for i in range(self._num_sprites):
            sprite_renderer = self._sprites[i]
            if sprite_renderer.is_dirty():
                self._load_vertex_properties(i)
                sprite_renderer.set_clean()
                rebuffer_data = True

        if rebuffer_data:
            gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self._vbo_id)
            gl.glBufferSubData(gl.GL_ARRAY_BUFFER, 0, self._vertices)

        self._shader.use()
        self._shader.upload_mat4("uProjection", camera.get_projection_matrix())
        self._shader.upload_mat4("uView", camera.get_view_matrix())

        for i in range(len(self._textures)):
            gl.glActiveTexture(self._texture_ids[i + 1])
            self._textures[i].bind()
        
        self._shader.upload_int_array("uTextures", self._tex_slots)

        gl.glBindVertexArray(self._vao_id)
        gl.glEnableVertexAttribArray(0)
        gl.glEnableVertexAttribArray(1)

        gl.glDrawElements(gl.GL_TRIANGLES, self._num_sprites * 6, gl.GL_UNSIGNED_INT, None)

        gl.glDisableVertexAttribArray(0)
        gl.glDisableVertexAttribArray(1)

        for texture in self._textures:
            texture.unbind()

        self._shader.detach()

    def _load_vertex_properties(self, index: int):
        sprite: SpriteRenderer = self._sprites[index]

        offset = index * 4 * self._VERTEX_SIZE

        color = sprite.get_color()
        tex_coords = sprite.get_tex_coords()
        tex_id = 0

        if sprite.get_texture() is not None:
            for i in range(len(self._textures)):
                if self._textures[i] == sprite.get_texture():
                    tex_id = i + 1
                    break

        x_add = 1.0
        y_add = 1.0

        for i in range(4):
            if i == 1:
                y_add = 0.0
            elif i == 2:
                x_add = 0.0
            elif i == 3:
                y_add = 1.0

            self._vertices[offset] = sprite.game_object.transform.position.x + (x_add * sprite.game_object.transform.scale.x)
            self._vertices[offset + 1] = sprite.game_object.transform.position.y + (y_add * sprite.game_object.transform.scale.y)

            self._vertices[offset + 2] = color.x
            self._vertices[offset + 3] = color.y
            self._vertices[offset + 4] = color.z
            self._vertices[offset + 5] = color.w

            self._vertices[offset + 6] = tex_coords[i].x
            self._vertices[offset + 7] = tex_coords[i].y

            self._vertices[offset + 8] = tex_id

            offset += self._VERTEX_SIZE

    def _generate_indices(self):
        elements = np.zeros(6 * self._max_batch_size, dtype=np.uint32)

        for i in range(self._max_batch_size):
            self._load_element_indices(elements, i)

        return elements

    def _load_element_indices(self, elements, index: int):
        offset_array_index = 6 * index
        offset = 4 * index

        elements[offset_array_index] = offset + 3
        elements[offset_array_index + 1] = offset + 2
        elements[offset_array_index + 2] = offset + 0

        elements[offset_array_index + 3] = offset + 0
        elements[offset_array_index + 4] = offset + 2
        elements[offset_array_index + 5] = offset + 1

    def has_room(self):
        return self._has_room

    def has_texture_room(self):
        return len(self._textures) < 8

    def has_texture(self, texture):
        return texture in self._textures

    def z_index(self):
        return self._z_index
