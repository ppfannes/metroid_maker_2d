import glm

class Camera:
    def __init__(self, position: glm.vec2):
        self._projection_matrix = glm.mat4(0.0)
        self._inverse_projection_matrix = glm.mat4(0.0)
        self._view_matrix = glm.mat4(0.0)
        self._inverse_view_matrix = glm.mat4(0.0)
        self._position = position
        self.adjust_projection()

    def adjust_projection(self):
        self._projection_matrix = glm.mat4(1.0)
        self._projection_matrix = glm.ortho(0.0, 32.0 * 40.0, 0.0, 32.0 * 21.0, 0.0, 100.0)
        self._inverse_projection_matrix = glm.inverse(self._projection_matrix)
    
    def get_view_matrix(self):
        camera_front = glm.vec3(0.0, 0.0, -1.0)
        camera_up = glm.vec3(0.0, 1.0, 0.0)
        self._view_matrix = glm.mat4(1.0)
        self._view_matrix = glm.lookAt(glm.vec3(self._position.x, self._position.y, 20.0),
                                                camera_front + glm.vec3(self._position.x, self._position.y, 0.0),
                                                camera_up)
        self._inverse_view_matrix = glm.inverse(self._view_matrix)

        return self._view_matrix

    def get_projection_matrix(self):
        return self._projection_matrix
    
    def get_inverse_projection(self):
        return self._inverse_projection_matrix
    
    def get_inverse_view(self):
        return self._inverse_view_matrix
