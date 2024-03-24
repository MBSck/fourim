from typing import Optional

import numpy as np
from PySide6.QtWidgets import QWidget, QHBoxLayout, QSlider, \
    QLineEdit, QLabel, QScrollArea, QVBoxLayout, QGridLayout
from PySide6.QtCore import Qt

from ..options import OPTIONS
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

    def __init__(self, parent: QWidget, name: str, unit: str,
                 min_value: float, max_value: float,
                 initial_value: Optional[float]) -> None:
        """The class's initialiser."""
        super().__init__()
        self.parent = parent
        self.scaling = np.diff([min_value, max_value])[0]*100

        main_layout = QVBoxLayout()
        
        label_layout = QHBoxLayout()
        unit = f" ({unit})" if unit else ""
        self.name, self.label, self.unit = name, QLabel(name), QLabel(unit)
        label_layout.addWidget(self.label)
        label_layout.addWidget(self.unit)
        main_layout.addLayout(label_layout)

        slider_layout = QHBoxLayout()
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(min_value*self.scaling)
        self.slider.setMaximum(max_value*self.scaling)
        self.slider.setValue(initial_value*self.scaling)
        self.slider.valueChanged.connect(self.updateLineEdit)
        
        self.lineEdit = QLineEdit(f"{initial_value:.2f}")
        self.lineEdit.returnPressed.connect(self.updateSliderFromLineEdit)
        
        slider_layout.addWidget(self.slider)
        slider_layout.addWidget(self.lineEdit)
        main_layout.addLayout(slider_layout)
        self.setLayout(main_layout)
        
    def updateLineEdit(self, value: float):
        """Updates the line edit with the new value."""
        self.lineEdit.setText(f"{value/self.scaling:.2f}")
        getattr(OPTIONS.model.active, self.name).value = value/self.scaling
        self.parent.parent.display_model()
        
    def updateSliderFromLineEdit(self):
        """Updates the slider with the new value."""
        value = round(float(self.lineEdit.text()), 2)
        self.slider.setValue(int(value*self.scaling))
        self.lineEdit.setText(f"{value:.2f}")


# TODO: Make a field to add multiple models and delte them as well
class ScrollBar(QWidget):
    """A scroll bar widget."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """The class constructor."""
        super().__init__(parent)
        self.parent = parent

        self.name = None
        self.sliders_grid = QGridLayout()
        self.sliders_container = QWidget()
        self.sliders = []

        self.main_layout = QVBoxLayout(self)
        self.update_scrollbar()
        self.sliders_container.setLayout(self.sliders_grid)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.sliders_container)
        self.main_layout.addWidget(self.scroll_area)

    def update_scrollbar(self):
        """Updates the scroll bar with new sliders
        depending on the model used."""
        model = set_active_model()
        model.fr.free = model.x.free = model.y.free = True
        model.inc.value = 1

        if self.name is not None:
            self.sliders_grid.removeWidget(self.name)
            self.name.deleteLater()

        if self.sliders:
            for slider in self.sliders:
                self.sliders_grid.removeWidget(slider)
                slider.deleteLater()
            self.sliders = []

        self.name = QLabel(f"{model.shortname}:")
        self.sliders_grid.addWidget(self.name, 0, 0)

        row, col, sliders_per_row = 1, 0, 4
        for param in model.get_params(free=True).values():
            slider = SliderWithInput(
                    self, param.shortname, str(param.unit),
                    param.min, param.max, param.value)
            self.sliders.append(slider)
            self.sliders_grid.addWidget(slider)

            slider.slider.setFixedWidth(200)
            slider.lineEdit.setFixedWidth(80)

            self.sliders_grid.addWidget(slider, row, col)
            col += 1
            if col >= sliders_per_row:
                col, row = 0, row+1
