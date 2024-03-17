import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget

from .tabs import SettingsTab, PlotTab
from ..options import OPTIONS


class MainWindow(QMainWindow):
    """Main window for the application."""

    def __init__(self):
        """The class's initialiser."""
        super().__init__()
        self.setWindowTitle("Fourim")
        self.setGeometry(100, 100, OPTIONS.geometry.width, OPTIONS.geometry.height)

        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)

        self.plot_tab = PlotTab(self)
        self.settings_tab = SettingsTab(self, plots=self.plot_tab)

        self.tab_widget.addTab(self.plot_tab, "Graphs")
        self.tab_widget.addTab(self.settings_tab, "Settings")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
