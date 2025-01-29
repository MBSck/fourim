import sys

from PySide6.QtWidgets import QApplication

from .backend.components import make_component
from .backend.options import OPTIONS
from .gui.main import MainWindow


# TODO: Implement more components
def main():
    OPTIONS.model.components.current[0] = make_component(OPTIONS.model.components.init)
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
