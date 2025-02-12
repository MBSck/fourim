import sys

from PySide6.QtWidgets import QApplication

from .backend.components import make_component
from .config.options import OPTIONS
from .gui.main import MainWindow


# TODO: Make issue for future features
def main():
    OPTIONS.model.components.current[0] = make_component(OPTIONS.model.components.init)
    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    window = MainWindow(screen.size().width(), screen.size().height())
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
