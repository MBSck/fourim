import sys

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QMainWindow

from ..options import OPTIONS


class MainWindow(QMainWindow):
    """Main window for the application."""

    def __init__(self):
        """The class constructor."""
        super().__init__()
        self.setWindowTitle("Fourim")
        self.setGeometry(100, 100, OPTIONS.geometry.width, OPTIONS.geometry.height)

        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        self.layout = QVBoxLayout(centralWidget) 

        self.params = []

        for param in ["x", "y"]:
            slider = SliderWithInput(param, 0, 100, 20)
            self.layout.addWidget(slider)
            self.params.append(slider)

        self.plot_canvas = LivePlotCanvas(self, width=5, height=4)
        self.layout.addWidget(self.plot_canvas)

        # Create multiple instances of the SliderWithInput
        
        # self.displayModeCombo = QComboBox()
        # self.displayModeCombo.addItems(["Side to Side", "Single"])
        # self.displayModeCombo.currentTextChanged.connect(self.displayModeChanged)
        # self.layout.addWidget(QLabel("Display Mode:"))
        # self.layout.addWidget(self.displayModeCombo)

        # self.dimensionalityCombo = QComboBox()
        # self.dimensionalityCombo.addItems(["1D", "2D"])
        # self.dimensionalityCombo.currentTextChanged.connect(self.dimensionalityChanged)
        # self.layout.addWidget(QLabel("Dimensionality:"))
        # self.layout.addWidget(self.dimensionalityCombo)

        # self.modelsCombo = QComboBox()
        # self.modelsCombo.addItems(OPTIONS.model.avail)
        # self.modelsCombo.currentIndexChanged.connect(self.modelChanged)
        # self.layout.addWidget(QLabel("Model:"))
        # self.layout.addWidget(self.modelsCombo)
        self.setLayout(self.layout)

    def displayModeChanged(self, text):
        print(f"Display Mode Changed to {text}")

    def dimensionalityChanged(self, text):
        print(f"Dimensionality Changed to {text}")

    def modelChanged(self, index):
        model = self.modelsCombo.itemText(index)

    def parameterChanged(self, value):
        print(f"Parameter Changed to {value}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
