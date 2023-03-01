import traceback
from metroid_maker.window import Window

def main() -> None:
    window = Window.get()

    try:
        window.run()
    except Exception:
        traceback.print_exc()
        input()

if __name__ == '__main__':
    main()
