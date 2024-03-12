from PySide6.QtWidgets import QWidget, QHBoxLayout, QSlider, QLineEdit, QLabel
from PySide6.QtCore import Qt


class SliderWithInput(QWidget):
    """A slider with an input field.

    Parameters
    ----------
    label : str
        The label of the slider.
    min_value : float
        The minimum value of the slider.
    max_value : float
        The maximum value of the slider.
    initial_value : float
        The initial value of the slider.
    """

    def __init__(self, label: str, min_value: float,
                 max_value: float, initial_value: float) -> None:
        """The class constructor."""
        super().__init__()
        self.layout = QHBoxLayout()
        
        self.label = QLabel(label)
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(min_value)
        self.slider.setMaximum(max_value)
        self.slider.setValue(initial_value)
        self.slider.valueChanged.connect(self.updateLineEdit)
        
        self.lineEdit = QLineEdit(str(initial_value))
        self.lineEdit.returnPressed.connect(self.updateSliderFromLineEdit)
        
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.slider)
        self.layout.addWidget(self.lineEdit)
        
        self.setLayout(self.layout)
        
    def updateLineEdit(self, value: float):
        """Updates the line edit with the new value."""
        self.lineEdit.setText(str(value))
        
    def updateSliderFromLineEdit(self):
        """Updates the slider with the new value."""
        value = int(self.lineEdit.text())
        self.slider.setValue(value)
