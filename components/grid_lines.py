import glm
from components.component import Component
from renderer.debug_draw import DebugDraw
from utils.settings import GRID_WIDTH, GRID_HEIGHT


class GridLines(Component):
    def editor_update(self, dt):
        from metroid_maker.window import Window

        camera = Window.get_scene().camera()
        camera_position = camera.get_position()
        projection_size = camera.get_projection_size()

        first_x = ((camera_position.x // GRID_WIDTH)) * GRID_WIDTH
        first_y = ((camera_position.y // GRID_HEIGHT)) * GRID_HEIGHT

        num_vertical_lines = ((projection_size.x * camera.get_zoom()) // GRID_WIDTH) + 2
        num_horizontal_lines = (
            (projection_size.y * camera.get_zoom()) // GRID_HEIGHT
        ) + 2

        height = projection_size.y * camera.get_zoom() + GRID_HEIGHT * 5
        width = projection_size.x * camera.get_zoom() + GRID_WIDTH * 5

        max_lines = int(max(num_vertical_lines, num_horizontal_lines))
        color = glm.fvec3(0.2, 0.2, 0.2)

        for i in range(max_lines):
            x = first_x + GRID_WIDTH * i
            y = first_y + GRID_HEIGHT * i

            if i < num_vertical_lines:
                DebugDraw.add_line_2d(
                    glm.fvec2(x, first_y), glm.fvec2(x, first_y + height), color=color
                )

            if i < num_horizontal_lines:
                DebugDraw.add_line_2d(
                    glm.fvec2(first_x, y), glm.fvec2(first_x + width, y), color=color
                )
