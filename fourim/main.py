import sys

from PySide6.QtWidgets import QApplication

from .backend.components import get_available_components
from .backend.options import OPTIONS
from .gui.main import MainWindow


def main():
    OPTIONS.model.components.avail = get_available_components()
    OPTIONS.model.components.current[0] = OPTIONS.model.components.avail["gaus"]

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
