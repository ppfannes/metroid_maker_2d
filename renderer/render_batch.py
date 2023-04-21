import ctypes
from functools import total_ordering
import math
import glm
import OpenGL.GL as gl

from components.sprite_renderer import SpriteRenderer


@total_ordering
class RenderBatch:
    def __init__(self, max_batch_size: int, z_index: int, renderer) -> None:
        self._POS_SIZE = 2
        self._COLOR_SIZE = 4
        self._TEX_COORDS_SIZE = 2
        self._TEX_ID_SIZE = 1
        self._ENTITY_ID_SIZE = 1

        self._POS_OFFSET = 0
        self._COLOR_OFFSET = self._POS_OFFSET + self._POS_SIZE * glm.sizeof(glm.float32)
        self._TEX_COORDS_OFFSET = self._COLOR_OFFSET + self._COLOR_SIZE * glm.sizeof(
            glm.float32
        )
        self._TEX_ID_OFFSET = (
            self._TEX_COORDS_OFFSET + self._TEX_COORDS_SIZE * glm.sizeof(glm.float32)
        )
        self._ENTITY_ID_OFFSET = self._TEX_ID_OFFSET + self._TEX_ID_SIZE * glm.sizeof(
            glm.float32
        )
        self._VERTEX_SIZE = 10
        self._VERTEX_SIZE_BYTES = self._VERTEX_SIZE * glm.sizeof(glm.float32)

        self._vao_id, self._vbo_id = 0, 0

        self._sprites = [SpriteRenderer() for _ in range(max_batch_size)]
        self._textures = []
        self._tex_slots = glm.array.from_numbers(glm.int32, 0, 1, 2, 3, 4, 5, 6, 7)
        self._max_batch_size = max_batch_size
        self._z_index = z_index
        self._renderer = renderer

        self._vertices = glm.array.zeros(
            max_batch_size * 4 * self._VERTEX_SIZE, glm.float32
        )

        self._num_sprites = 0
        self._has_room = True
        self._texture_ids = [
            gl.GL_TEXTURE0,
            gl.GL_TEXTURE1,
            gl.GL_TEXTURE2,
            gl.GL_TEXTURE3,
            gl.GL_TEXTURE4,
            gl.GL_TEXTURE5,
            gl.GL_TEXTURE6,
            gl.GL_TEXTURE7,
            gl.GL_TEXTURE8,
        ]

    def __lt__(self, other: "RenderBatch"):
        return self._z_index < other._z_index

    def start(self):
        self._vao_id = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self._vao_id)

        self._vbo_id = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self._vbo_id)
        gl.glBufferData(
            gl.GL_ARRAY_BUFFER,
            self._vertices.nbytes,
            self._vertices.ptr,
            gl.GL_DYNAMIC_DRAW,
        )

        ebo_id = gl.glGenBuffers(1)
        indices = self._generate_indices()
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, ebo_id)
        gl.glBufferData(
            gl.GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices.ptr, gl.GL_STATIC_DRAW
        )

        gl.glVertexAttribPointer(
            0,
            self._POS_SIZE,
            gl.GL_FLOAT,
            False,
            self._VERTEX_SIZE_BYTES,
            ctypes.c_void_p(self._POS_OFFSET),
        )
        gl.glEnableVertexAttribArray(0)

        gl.glVertexAttribPointer(
            1,
            self._COLOR_SIZE,
            gl.GL_FLOAT,
            False,
            self._VERTEX_SIZE_BYTES,
            ctypes.c_void_p(self._COLOR_OFFSET),
        )
        gl.glEnableVertexAttribArray(1)

        gl.glVertexAttribPointer(
            2,
            self._TEX_COORDS_SIZE,
            gl.GL_FLOAT,
            False,
            self._VERTEX_SIZE_BYTES,
            ctypes.c_void_p(self._TEX_COORDS_OFFSET),
        )
        gl.glEnableVertexAttribArray(2)

        gl.glVertexAttribPointer(
            3,
            self._TEX_ID_SIZE,
            gl.GL_FLOAT,
            False,
            self._VERTEX_SIZE_BYTES,
            ctypes.c_void_p(self._TEX_ID_OFFSET),
        )
        gl.glEnableVertexAttribArray(3)

        gl.glVertexAttribPointer(
            4,
            self._ENTITY_ID_SIZE,
            gl.GL_FLOAT,
            False,
            self._VERTEX_SIZE_BYTES,
            ctypes.c_void_p(self._ENTITY_ID_OFFSET),
        )
        gl.glEnableVertexAttribArray(4)

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

    def destroy_if_exists(self, game_object):
        sprite_renderer = game_object.get_component(SpriteRenderer)

        for i, sprite in enumerate(self._sprites):
            if sprite == sprite_renderer:
                self._sprites.pop(i)
                for new_sprite in self._sprites[i:]:
                    new_sprite.set_dirty()
                self._num_sprites -= 1
                return True
        return False

    def render(self):
        from metroid_maker.window import Window
        from renderer.renderer import Renderer

        rebuffer_data = False
        for i in reversed(range(self._num_sprites)):
            sprite_renderer = self._sprites[i]
            if sprite_renderer.is_dirty():
                if not self.has_texture(sprite_renderer.get_texture()):
                    self._renderer.destroy_game_object(sprite_renderer.game_object)
                    self._renderer.add_game_object(sprite_renderer.game_object)
                else:
                    self._load_vertex_properties(i)
                    sprite_renderer.set_clean()
                    rebuffer_data = True

                if sprite_renderer.game_object.transform.z_index != self._z_index:
                    self.destroy_if_exists(sprite_renderer.game_object)
                    self._renderer.add_game_object(sprite_renderer.game_object)

        if rebuffer_data:
            gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self._vbo_id)
            gl.glBufferSubData(
                gl.GL_ARRAY_BUFFER,
                0,
                size=self._vertices.nbytes,
                data=self._vertices.ptr,
            )

        shader = Renderer.get_bound_shader()
        shader.upload_fmat4(
            "uProjection", Window.get_scene().camera().get_projection_matrix()
        )
        shader.upload_fmat4("uView", Window.get_scene().camera().get_view_matrix())

        for i, texture in enumerate(self._textures):
            gl.glActiveTexture(self._texture_ids[i + 1])
            texture.bind()

        shader.upload_int_array("uTextures", self._tex_slots)

        gl.glBindVertexArray(self._vao_id)
        gl.glEnableVertexAttribArray(0)
        gl.glEnableVertexAttribArray(1)

        gl.glDrawElements(
            gl.GL_TRIANGLES, self._num_sprites * 6, gl.GL_UNSIGNED_INT, None
        )

        gl.glDisableVertexAttribArray(0)
        gl.glDisableVertexAttribArray(1)

        for texture in self._textures:
            texture.unbind()

        shader.detach()

    def _load_vertex_properties(self, index: int):
        sprite: SpriteRenderer = self._sprites[index]

        offset = index * 4 * self._VERTEX_SIZE

        color = sprite.get_color()
        tex_coords = sprite.get_tex_coords()
        tex_id = 0

        if sprite.get_texture() is not None:
            for i, texture in enumerate(self._textures):
                if texture == sprite.get_texture():
                    tex_id = i + 1
                    break

        is_rotated = sprite.game_object.transform.rotation != 0.0
        transform_matrix = glm.identity(glm.mat4)

        if is_rotated:
            transform_matrix = glm.translate(
                transform_matrix, glm.fvec3(sprite.game_object.transform.position, 0.0)
            )
            transform_matrix = glm.rotate(
                transform_matrix,
                math.radians(sprite.game_object.transform.rotation),
                glm.fvec3(0.0, 0.0, 1.0),
            )
            transform_matrix = glm.scale(
                transform_matrix, glm.fvec3(sprite.game_object.transform.scale, 1.0)
            )

        x_add = 0.5
        y_add = 0.5

        for i in range(4):
            if i == 1:
                y_add = -0.5
            elif i == 2:
                x_add = -0.5
            elif i == 3:
                y_add = 0.5

            current_pos = glm.fvec4(
                sprite.game_object.transform.position.x
                + (x_add * sprite.game_object.transform.scale.x),
                sprite.game_object.transform.position.y
                + (y_add * sprite.game_object.transform.scale.y),
                0.0,
                1.0,
            )

            if is_rotated:
                current_pos = glm.mul(
                    transform_matrix, glm.fvec4(x_add, y_add, 0.0, 1.0)
                )

            self._vertices[offset] = current_pos.x
            self._vertices[offset + 1] = current_pos.y

            self._vertices[offset + 2] = color.x
            self._vertices[offset + 3] = color.y
            self._vertices[offset + 4] = color.z
            self._vertices[offset + 5] = color.w

            self._vertices[offset + 6] = tex_coords[i].x
            self._vertices[offset + 7] = tex_coords[i].y

            self._vertices[offset + 8] = tex_id

            self._vertices[offset + 9] = sprite.game_object.get_uid() + 1

            offset += self._VERTEX_SIZE

    def _generate_indices(self):
        elements = glm.array.zeros(6 * self._max_batch_size, glm.uint32)

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
