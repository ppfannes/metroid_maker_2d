import imgui
from observers.event_system import EventSystem
from observers.events.event import Event
from observers.events.event_type import EventType


class MenuBar:
    def imgui(self):
        if imgui.begin_menu_bar():
            if imgui.begin_menu("File"):
                clicked_save, _ = imgui.menu_item("Save", "Ctrl+S")
                clicked_load, _ = imgui.menu_item("Load", "Ctrl+O")

                if clicked_save:
                    EventSystem.notify(None, Event(EventType.SAVE_LEVEL))

                if clicked_load:
                    EventSystem.notify(None, Event(EventType.LOAD_LEVEL))

                imgui.end_menu()

            imgui.end_menu_bar()
