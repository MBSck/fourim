from typing import Optional

import numpy as np
from PySide6.QtWidgets import QWidget, QHBoxLayout, QSlider, \
    QLineEdit, QLabel, QScrollArea, QVBoxLayout, QComboBox, QRadioButton
from PySide6.QtCore import Qt

from ..options import OPTIONS
from ..utils import set_active_model


# TODO: Scale slider for every input
# TODO: Start slider field with correct value
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
                 initial_value: Optional[float] = None) -> None:
        """The class's initialiser."""
        super().__init__()
        self.parent = parent

        self.scaling = 1
        if min_value == 0 and max_value == 1:
            self.scaling = 10
        else:
            self.scaling = 10*np.diff([min_value, max_value])[0]

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
        
        self.lineEdit = QLineEdit(f"{initial_value/self.scaling:.2f}")
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
        value = int(self.lineEdit.text())
        self.slider.setValue(value/scaling)


# TODO: Make a field to add multiple models
# TODO: Make slider possible for 2 digits after decimal point
class ScrollBar(QWidget):
    """A scroll bar widget."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """The class constructor."""
        super().__init__(parent)
        self.parent = parent
        self.sliders_layout = QVBoxLayout()
        self.sliders_container = QWidget()
        self.sliders = []

        main_layout = QVBoxLayout(self)
        title_model = QLabel("Model:")
        self.model = QComboBox()
        for model in OPTIONS.model.avail:
            self.model.addItem(model)

        self.model.setCurrentIndex(0)
        self.selectedOption = self.model.currentText()
        self.model.currentIndexChanged.connect(lambda: self.change_model())
        main_layout.addWidget(title_model)
        main_layout.addWidget(self.model)

        self.update_scrollbar()
        self.sliders_container.setLayout(self.sliders_layout)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.sliders_container)

        main_layout.addWidget(self.scroll_area)

        title_dim = QLabel("Plot Dimension:")
        hLayout = QHBoxLayout()

        self.one_dim_radio = QRadioButton("1D")
        self.one_dim_radio.toggled.connect(self.toggle_dimension)
        self.one_dim_radio.setChecked(OPTIONS.display.one_dimensional)
        hLayout.addWidget(self.one_dim_radio)

        self.two_dim_radio = QRadioButton("2D")
        self.two_dim_radio.toggled.connect(self.toggle_dimension)
        self.two_dim_radio.setChecked(not OPTIONS.display.one_dimensional)
        hLayout.addWidget(self.two_dim_radio)
        main_layout.addWidget(title_dim)
        main_layout.addLayout(hLayout)

    def change_model(self) -> None:
        """Slot for model change."""
        OPTIONS.model.selected = self.model.currentText()
        set_active_model()
        self.update_scrollbar()
        self.parent.display_model()

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
        model.inc.value = 0

        for param in model.get_params(free=True).values():
            slider = SliderWithInput(
                    self, param.shortname, str(param.unit),
                    param.min, param.max, param.value)
            self.sliders.append(slider)
            self.sliders_layout.addWidget(slider)

    def toggle_dimension(self) -> None:
        """Slot for radio buttons toggled."""
        if self.one_dim_radio.isChecked():
            OPTIONS.display.one_dimensional = True
        elif self.two_dim_radio.isChecked():
            OPTIONS.display.one_dimensional = False
        self.parent.display_model()
