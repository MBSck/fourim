from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QMainWindow, QTabWidget

from .plot import PlotTab
from .settings import SettingsTab


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

    def __init__(self, width: int, height: int):
        """The class's initialiser."""
        super().__init__()
        self.setWindowTitle("Fourim")
        self.setWindowIcon(QIcon(QPixmap("../../assets/icon.png")))
        self.setGeometry(100, 100, width, height)

        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)

        self.plot_tab = PlotTab(self)
        self.settings_tab = SettingsTab(self)

        self.tab_widget.addTab(self.plot_tab, "Graphs")
        self.tab_widget.addTab(self.settings_tab, "Settings")
