import glm

class Camera:
    def __init__(self, position: glm.vec2):
        self._projection_matrix = glm.fmat4(0.0)
        self._projection_width = 6.0
        self._projection_height = 3.0
        self._projection_size = glm.fvec2(self._projection_width, self._projection_height)
        self._inverse_projection_matrix = glm.fmat4(0.0)
        self._view_matrix = glm.fmat4(0.0)
        self._inverse_view_matrix = glm.fmat4(0.0)
        self._position = position
        self._zoom = 1.0
        self.adjust_projection()

    def adjust_projection(self):
        self._projection_matrix = glm.identity(glm.fmat4)
        self._projection_matrix = glm.ortho(0.0, self._projection_size.x * self._zoom, 0.0, self._projection_size.y * self._zoom, 0.0, 100.0)
        self._inverse_projection_matrix = glm.inverse(self._projection_matrix)

    def get_view_matrix(self):
        camera_front = glm.fvec3(0.0, 0.0, -1.0)
        camera_up = glm.fvec3(0.0, 1.0, 0.0)
        self._view_matrix = glm.identity(glm.fmat4)
        self._view_matrix = glm.lookAt(glm.fvec3(self._position.x, self._position.y, 20.0),
                                                glm.add(camera_front, glm.fvec3(self._position.x, self._position.y, 0.0)),
                                                camera_up)
        self._inverse_view_matrix = glm.inverse(self._view_matrix)

        return self._view_matrix

    def get_projection_matrix(self):
        return self._projection_matrix

    def get_inverse_projection(self):
        return self._inverse_projection_matrix
    
    def get_inverse_view(self):
        return self._inverse_view_matrix
    
    def get_position(self):
        return self._position
    
    def get_projection_size(self):
        return self._projection_size
    
    def get_zoom(self):
        return self._zoom
    
    def set_zoom(self, value):
        self._zoom = value

    def add_zoom(self, add_zoom):
        self._zoom += add_zoom
