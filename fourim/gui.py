import sys

import matplotlib

matplotlib.use('Qt5Agg')

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QComboBox, QSlider
from PySide6.QtCore import Qt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from .options import OPTIONS


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        sc = MplCanvas(self, width=5, height=4, dpi=300)
        sc.axes.plot([0,1,2,3,4], [10,1,20,3,40])
        self.setCentralWidget(sc)

        self.show()



class ExampleWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fourim")
        self.setGeometry(100, 100, 400, 300)

        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        layout = QVBoxLayout(centralWidget)

        self.displayModeCombo = QComboBox()
        self.displayModeCombo.addItems(["Side to Side", "Single"])
        self.displayModeCombo.currentTextChanged.connect(self.displayModeChanged)
        layout.addWidget(QLabel("Display Mode:"))
        layout.addWidget(self.displayModeCombo)

        self.dimensionalityCombo = QComboBox()
        self.dimensionalityCombo.addItems(["1D", "2D"])
        self.dimensionalityCombo.currentTextChanged.connect(self.dimensionalityChanged)
        layout.addWidget(QLabel("Dimensionality:"))
        layout.addWidget(self.dimensionalityCombo)

        self.modelsCombo = QComboBox()
        self.modelsCombo.addItems(OPTIONS.model.avail)
        self.modelsCombo.currentIndexChanged.connect(self.modelChanged)
        layout.addWidget(QLabel("Model:"))
        layout.addWidget(self.modelsCombo)

        self.parameterControl = QSlider()
        self.parameterControl.setOrientation(Qt.Horizontal)
        self.parameterControl.setMinimum(1)
        self.parameterControl.setMaximum(100)
        self.parameterControl.valueChanged.connect(self.parameterChanged)
        layout.addWidget(QLabel("Parameter:"))
        layout.addWidget(self.parameterControl)

    def displayModeChanged(self, text):
        print(f"Display Mode Changed to {text}")
        # Call relevant function or update UI based on display mode.

    def dimensionalityChanged(self, text):
        print(f"Dimensionality Changed to {text}")
        # Update UI or functionality based on dimensionality.

    def modelChanged(self, index):
        print(f"Model Changed to {self.modelsCombo.itemText(index)}")
        # Could reset parameters or update UI based on the model selection.

    def parameterChanged(self, value):
        print(f"Parameter Changed to {value}")
        # Functionality that reacts to parameter changes, such as updating a model or display.


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExampleWindow()
    window.show()
    sys.exit(app.exec())
