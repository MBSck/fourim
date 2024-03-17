from typing import Optional

from PySide6.QtWidgets import QWidget, QHBoxLayout, QSlider, \
    QLineEdit, QLabel, QScrollArea, QVBoxLayout
from PySide6.QtCore import Qt

from ..utils import set_active_model


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

    def __init__(self, name: str, unit: str, min_value: float,
                 max_value: float, initial_value: float) -> None:
        """The class's initialiser."""
        super().__init__()
        main_layout = QVBoxLayout()
        
        label_layout = QHBoxLayout()
        unit = f" ({unit})" if unit else ""
        self.name, self.unit = QLabel(name), QLabel(unit)
        label_layout.addWidget(self.name)
        label_layout.addWidget(self.unit)
        main_layout.addLayout(label_layout)

        slider_layout = QHBoxLayout()
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(min_value)
        self.slider.setMaximum(max_value)
        self.slider.setValue(initial_value)
        self.slider.valueChanged.connect(self.updateLineEdit)
        
        self.lineEdit = QLineEdit(str(initial_value))
        self.lineEdit.returnPressed.connect(self.updateSliderFromLineEdit)
        
        slider_layout.addWidget(self.slider)
        slider_layout.addWidget(self.lineEdit)
        main_layout.addLayout(slider_layout)
        self.setLayout(main_layout)
        
    def updateLineEdit(self, value: float):
        """Updates the line edit with the new value."""
        self.lineEdit.setText(str(value))
        
    def updateSliderFromLineEdit(self):
        """Updates the slider with the new value."""
        value = int(self.lineEdit.text())
        self.slider.setValue(value)


# TODO: Make a field to add multiple models
# TODO: Make slider possible for 2 digits after decimal point
class ScrollBar(QWidget):
    """A scroll bar widget."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """The class constructor."""
        super().__init__(parent)
        self.sliders_layout = QVBoxLayout()
        self.sliders_container = QWidget()
        self.sliders = []
        self.update_scrollbar()
        self.sliders_container.setLayout(self.sliders_layout)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.sliders_container)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.scroll_area)

    def update_scrollbar(self):
        """Updates the scroll bar with new sliders
        depending on the model used."""
        if self.sliders:
            for slider in self.sliders:
                slider.deleteLater()
            self.sliders = []

        model = set_active_model()
        model.fr.free = True
        model.x.free = model.y.free = True
        model.inc.free = model.pa.free = True

        for param in model.get_params(free=True).values():
            slider = SliderWithInput(
                    param.shortname, str(param.unit),
                    param.min, param.max, param.value)
            self.sliders.append(slider)
            self.sliders_layout.addWidget(slider)


