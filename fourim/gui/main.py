import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget

from .tabs import SettingsTab, PlotTab
from ..options import OPTIONS
from ..utils import ComponentManager, FileManager, get_available_components


class MainWindow(QMainWindow):
    """Main window for the application.

    Attributes
    ----------
    component_manager : ComponentManager
        A manager for the components in the application.
    file_manager : FileManager
        A manager for the files in the application.
    tab_widget : QTabWidget
        The tab widget for the main window.
    plot_tab : PlotTab
        The tab for plotting graphs.
    settings_tab : SettingsTab
        The tab for the settings.
    """

    def __init__(self):
        """The class's initialiser."""
        super().__init__()
        OPTIONS.model.components.avail = get_available_components()
        self.component_manager = ComponentManager()
        self.component_manager.add_component("PointSource")
        self.file_manager = FileManager()

        self.setWindowTitle("Fourim")
        self.setGeometry(100, 100, OPTIONS.geometry.width, OPTIONS.geometry.height)

        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)

        self.plot_tab = PlotTab(self)
        self.settings_tab = SettingsTab(self)

        self.tab_widget.addTab(self.plot_tab, "Graphs")
        self.tab_widget.addTab(self.settings_tab, "Settings")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
