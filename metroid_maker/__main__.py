import traceback
from metroid_maker.window import Window
import imgui
import glfw
import OpenGL.GL as gl


def main() -> None:
    window = Window.get()

    try:
        window.run()
    except Exception:
        traceback.print_exc()
        input()

    # def impl_glfw_init():
    #     width, height = 1280, 720
    #     window_name = "minimal ImGui/GLFW3 example"

    #     if not glfw.init():
    #         print("Could not initialize OpenGL context")
    #         exit(1)

    #     # Create a windowed mode window and its OpenGL context
    #     window = glfw.create_window(int(width), int(height), window_name, None, None)
    #     glfw.make_context_current(window)

    #     if not window:
    #         glfw.terminate()
    #         print("Could not initialize Window")
    #         exit(1)

    #     return window

    # imgui.create_context()
    # window = impl_glfw_init()
    # impl = imgui.integrations.glfw.GlfwRenderer(window)
    # while not glfw.window_should_close(window):
    #     glfw.poll_events()
    #     impl.process_inputs()

    #     imgui.new_frame()

    #     imgui.begin("test")

    #     imgui.button("source")
    #     if imgui.begin_drag_drop_source():
    #         imgui.set_drag_drop_payload("itemtype", b"payload")
    #         print(imgui.get_drag_drop_payload())
    #         imgui.button("dragged source")
    #         imgui.end_drag_drop_source()

    #     imgui.button("dest")
    #     if imgui.begin_drag_drop_target():
    #         payload = imgui.accept_drag_drop_payload("itemtype")
    #         print(imgui.get_drag_drop_payload())
    #         if payload is not None:
    #             print(f"Payload accepted '{payload}'")
    #         imgui.end_drag_drop_target()

    #     imgui.end()

    #     gl.glClearColor(1.0, 1.0, 1.0, 1.0)
    #     gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    #     imgui.render()
    #     impl.render(imgui.get_draw_data())
    #     glfw.swap_buffers(window)

    # impl.shutdown()
    # glfw.terminate()


if __name__ == "__main__":
    main()
