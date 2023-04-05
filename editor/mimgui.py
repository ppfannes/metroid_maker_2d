import glm
import imgui


class MImGui:
    @classmethod
    def draw_vec2_control(cls, label, values, reset_value=0.0, column_width=220.0):
        imgui.push_id(label)

        imgui.columns(2)
        imgui.set_column_width(0, column_width)
        imgui.text(label.capitalize())
        imgui.next_column()

        imgui.push_style_var(imgui.STYLE_ITEM_SPACING, (0.0, 0.0))

        line_height = imgui.get_font_size() + imgui.get_style().frame_padding[1] * 2.0
        button_size = glm.fvec2(line_height + 3.0, line_height)
        width_each = (imgui.calculate_item_width() - button_size.x * 2.0) / 2.0

        imgui.push_item_width(width_each)
        imgui.push_style_color(imgui.COLOR_BUTTON, 0.8, 0.1, 0.15, 1.0)
        imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, 0.9, 0.2, 0.2, 1.0)
        imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, 0.8, 0.1, 0.15, 1.0)
        if imgui.button("X", button_size.x, button_size.y):
            values.x = reset_value
        imgui.pop_style_color(3)

        imgui.same_line()
        changed, value = imgui.drag_float("##x", values.x, change_speed=0.1)
        if changed:
            values.x = value
        imgui.pop_item_width()
        imgui.same_line()

        imgui.push_item_width(width_each)
        imgui.push_style_color(imgui.COLOR_BUTTON, 0.2, 0.7, 0.2, 1.0)
        imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, 0.3, 0.8, 0.3, 1.0)
        imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, 0.2, 0.8, 0.2, 1.0)
        if imgui.button("Y", button_size.x, button_size.y):
            values.y = reset_value
        imgui.pop_style_color(3)

        imgui.same_line()
        changed, value = imgui.drag_float("##y", values.y, change_speed=0.1)
        if changed:
            values.y = value
        imgui.pop_item_width()
        imgui.same_line()

        imgui.next_column()

        imgui.pop_style_var()
        imgui.columns(1)
        imgui.pop_id()

        return values

    @classmethod
    def draw_vec3_control(cls, label, values, reset_value=0.0, column_width=220.0):
        imgui.push_id(label)

        imgui.columns(3)
        imgui.set_column_width(0, column_width)
        imgui.text(label.capitalize())
        imgui.next_column()

        imgui.push_style_var(imgui.STYLE_ITEM_SPACING, (0.0, 0.0))

        line_height = imgui.get_font_size() + imgui.get_style().frame_padding[1] * 2.0
        button_size = glm.fvec2(line_height + 3.0, line_height)
        width_each = (imgui.calculate_item_width() - button_size.x * 2.0) / 2.0

        imgui.push_item_width(width_each)
        imgui.push_style_color(imgui.COLOR_BUTTON, 0.8, 0.1, 0.15, 1.0)
        imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, 0.9, 0.2, 0.2, 1.0)
        imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, 0.8, 0.1, 0.15, 1.0)
        if imgui.button("X", button_size.x, button_size.y):
            values.x = reset_value
        imgui.pop_style_color(3)

        imgui.same_line()
        changed, value = imgui.drag_float("##x", values.x, change_speed=0.1)
        if changed:
            values.x = value
        imgui.pop_item_width()
        imgui.same_line()

        imgui.push_item_width(width_each)
        imgui.push_style_color(imgui.COLOR_BUTTON, 0.2, 0.7, 0.2, 1.0)
        imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, 0.3, 0.8, 0.3, 1.0)
        imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, 0.2, 0.8, 0.2, 1.0)
        if imgui.button("Y", button_size.x, button_size.y):
            values.y = reset_value
        imgui.pop_style_color(3)

        imgui.same_line()
        changed, value = imgui.drag_float("##y", values.y, change_speed=0.1)
        if changed:
            values.y = value
        imgui.pop_item_width()
        imgui.same_line()

        imgui.push_item_width(width_each)
        imgui.push_style_color(imgui.COLOR_BUTTON, 0.1, 0.25, 0.8, 1.0)
        imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, 0.2, 0.35, 0.9, 1.0)
        imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, 0.1, 0.25, 0.8, 1.0)
        if imgui.button("Z", button_size.x, button_size.y):
            values.z = reset_value
        imgui.pop_style_color(3)

        imgui.same_line()
        changed, value = imgui.drag_float("##z", values.z, change_speed=0.1)
        if changed:
            values.z = value
        imgui.pop_item_width()
        imgui.same_line()

        imgui.next_column()

        imgui.pop_style_var()
        imgui.columns(1)
        imgui.pop_id()

        return values

    @classmethod
    def drag_float(cls, label, value, column_width=220.0):
        imgui.push_id(label)

        imgui.columns(2)
        imgui.set_column_width(0, column_width)
        imgui.text(label.capitalize())
        imgui.next_column()

        changed, val = imgui.drag_float("##drag_float", value, change_speed=0.1)
        if changed:
            value = val

        imgui.columns(1)
        imgui.pop_id()

        return value

    @classmethod
    def drag_int(cls, label, value, column_width=220.0):
        imgui.push_id(label)

        imgui.columns(2)
        imgui.set_column_width(0, column_width)
        imgui.text(label.capitalize())
        imgui.next_column()

        changed, val = imgui.drag_int("##drag_int", value, change_speed=0.1)
        if changed:
            value = val

        imgui.columns(1)
        imgui.pop_id()

        return value

    @classmethod
    def color_picker4(cls, label, values, column_width=220.0):
        imgui.push_id(label)

        imgui.columns(2)
        imgui.set_column_width(0, column_width)
        imgui.text(label.capitalize())
        imgui.next_column()

        changed, value = imgui.color_edit4("##color_picker", *values.to_tuple())
        if changed:
            values = glm.fvec4(*value)

        imgui.columns(1)
        imgui.pop_id()

        return values

    @classmethod
    def input_text(cls, label, value, column_width=220.0):
        imgui.push_id(label)

        imgui.columns(2)
        imgui.set_column_width(0, column_width)
        imgui.text(label.capitalize())
        imgui.next_column()

        changed, val = imgui.input_text("##" + label, value, 256)
        if changed:
            imgui.columns(1)
            imgui.pop_id()

            return val

        imgui.columns(1)
        imgui.pop_id()

        return value
