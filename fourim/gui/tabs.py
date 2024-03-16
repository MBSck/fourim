from typing import Optional

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, \
    QGridLayout, QRadioButton, QHBoxLayout

from .plot import MplCanvas
from .slider import ScrollBar
from ..options import OPTIONS


class SettingsTab(QWidget):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout()

        title = QLabel("Dimensionality:")
        hLayout = QHBoxLayout()

        self.radio1 = QRadioButton("1D")
        self.radio1.toggled.connect(self.onRadioToggled)
        hLayout.addWidget(self.radio1)

        self.radio2 = QRadioButton("2D")
        self.radio2.toggled.connect(self.onRadioToggled)
        hLayout.addWidget(self.radio2)

        layout.addWidget(title)
        layout.addLayout(hLayout)
        self.setLayout(layout)

    def onRadioToggled(self):
        """Slot for radio buttons toggled."""
        if self.radio1.isChecked():
            OPTIONS.display.one_dimensional = True
        elif self.radio2.isChecked():
            OPTIONS.display.one_dimensional = False

    def displayModeChanged(self, text):
        print(f"Display Mode Changed to {text}")

    def dimensionalityChanged(self, text):
        print(f"Dimensionality Changed to {text}")


class PlotTab(QWidget):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        layout = QGridLayout()

        self.canvas_left = MplCanvas(self, width=5, height=4, dpi=100)
        self.canvas_right = MplCanvas(self, width=5, height=4, dpi=100)
        self.scroll_bar = ScrollBar(self)
        layout.addWidget(self.canvas_left, 0, 0)
        layout.addWidget(self.canvas_right, 0, 1)
        layout.addWidget(self.scroll_bar, 0, 2)
        self.setLayout(layout)

    def modelChanged(self, index):
        ...

    def parameterChanged(self, value):
        ...
