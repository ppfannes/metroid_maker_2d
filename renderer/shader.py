import os
import fnmatch
import glm
import numpy as np
import OpenGL.GL as gl
import OpenGL.GL.shaders as shaders

class Shader:
    def __init__(self, file_path: str, shader_name:str):
        self._file_path = file_path
        self._vertex_source = ""
        self._fragment_source = ""
        self._shader_program_id = None

        try:
            for fname in os.listdir(self._file_path):
                if fnmatch.fnmatch(fname, shader_name + "_vertex.glsl"):
                    with open(self._file_path + "/" + fname, "r") as f:
                        self._vertex_source = f.readlines()
                elif fnmatch.fnmatch(fname, shader_name + "_fragment.glsl"):
                    with open(self._file_path + "/" + fname, "r") as f:
                        self._fragment_source = f.readlines()

        except IOError:
            raise ValueError("Shader collection failed " + self._file_path)

    def compile(self):

        vertex_id = shaders.compileShader(self._vertex_source, gl.GL_VERTEX_SHADER)
        success = gl.glGetShaderiv(vertex_id, gl.GL_COMPILE_STATUS)

        if success == gl.GL_FALSE:
            raise RuntimeError(gl.glGetShaderInfoLog(vertex_id))

        fragment_id = shaders.compileShader(self._fragment_source, gl.GL_FRAGMENT_SHADER)
        success = gl.glGetShaderiv(vertex_id, gl.GL_COMPILE_STATUS)

        if success == gl.GL_FALSE:
            raise RuntimeError(gl.glGetShaderInfoLog(fragment_id))

        self._shader_program_id = shaders.compileProgram(vertex_id, fragment_id)

        success = gl.glGetProgramiv(self._shader_program_id, gl.GL_LINK_STATUS)

        if success == gl.GL_FALSE:
            raise RuntimeError(gl.glGetProgramInfoLog(self._shader_program_id))

    def use(self):
        gl.glUseProgram(self._shader_program_id)

    def detach(self):
        gl.glUseProgram(0)

    def upload_fmat4(self, var_name: str, mat4: glm.fmat4):
        self.use()
        gl.glUniformMatrix4fv(gl.glGetUniformLocation(self._shader_program_id, var_name), 1, gl.GL_FALSE, glm.value_ptr(mat4))

    def upload_fmat3(self, var_name: str, mat3: glm.fmat3):
        self.use()
        gl.glUniformMatrix3fv(gl.glGetUniformLocation(self._shader_program_id, var_name), 1, gl.GL_FALSE, glm.value_ptr(mat3))

    def upload_fvec4(self, var_name: str, vec4: glm.fvec4):
        self.use()
        gl.glUniform4f(gl.glGetUniformLocation(self._shader_program_id, var_name), vec4.x, vec4.y, vec4.z, vec4.w)

    def upload_fvec3(self, var_name: str, vec3: glm.fvec3):
        self.use()
        gl.glUniform3f(gl.glGetUniformLocation(self._shader_program_id, var_name), vec3.x, vec3.y, vec3.z)

    def upload_fvec2(self, var_name: str, vec2: glm.fvec2):
        self.use()
        gl.glUniform2f(gl.glGetUniformLocation(self._shader_program_id, var_name), vec2.x, vec2.y)

    def upload_float32(self, var_name: str, val: glm.float32):
        self.use()
        gl.glUniform1f(gl.glGetUniformLocation(self._shader_program_id, var_name), val)

    def upload_int32(self, var_name: str, val: glm.int32):
        self.use()
        gl.glUniform1i(gl.glGetUniformLocation(self._shader_program_id, var_name), val)

    def upload_texture(self, var_name: str, slot: glm.int32):
        self.use()
        gl.glUniform1i(gl.glGetUniformLocation(self._shader_program_id, var_name), slot)

    def upload_int_array(self, var_name: str, array: glm.array):
        self.use()
        gl.glUniform1iv(gl.glGetUniformLocation(self._shader_program_id, var_name), array.nbytes, array.ptr)
