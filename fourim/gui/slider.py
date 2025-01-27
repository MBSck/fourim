from types import SimpleNamespace
from typing import Callable, Optional

import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from ..backend.options import OPTIONS


class SliderWithInput(QWidget):
    """A slider with an input field.

    Parameters
    ----------
    param : types.SimpleNamespace
        The simple namespace containing the parameter information.
    update_function : Callable, optional
        The function to call when the slider value changes.
    index : int, optional
        The index of the model component.

    Attributes
    ----------
    parent : QWidget
        The parent widget.
    index : int
        The index of the model component.
    scaling : float
        The scaling factor.
    param : types.SimpleNamespace
        The simple namespace containing the parameter information.
    unit : QLabel
        The unit of the parameter.
    slider : QSlider
        The slider.
    lineEdit : QLineEdit
        The input field.
    """

    def __init__(
        self,
        parent: QWidget,
        param: SimpleNamespace,
        update_function: Optional[Callable] = None,
        index: Optional[int] = None,
    ) -> None:
        """The class's initialiser."""
        super().__init__()
        self.parent, self.index = parent, index
        self.scaling = np.diff([param.min, param.max])[0] * 100

        main_layout = QVBoxLayout()
        label_layout = QHBoxLayout()
        self.name = param.name
        self.unit = QLabel(str(param.unit))
        label_layout.addWidget(QLabel(param.name))
        label_layout.addWidget(self.unit)
        main_layout.addLayout(label_layout)

        slider_layout = QHBoxLayout()
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(param.min * self.scaling)
        self.slider.setMaximum(param.max * self.scaling)
        self.slider.setValue(param.value * self.scaling)
        self.slider.valueChanged.connect(
            self.updateLineEdit if update_function is None else update_function
        )

        self.lineEdit = QLineEdit(f"{param.value:.2f}")
        self.lineEdit.returnPressed.connect(self.updateSliderFromLineEdit)

        slider_layout.addWidget(self.slider)
        slider_layout.addWidget(self.lineEdit)
        main_layout.addLayout(slider_layout)
        self.setLayout(main_layout)

    def updateLineEdit(self, value: float):
        """Updates the line edit with the new value."""
        self.lineEdit.setText(f"{value / self.scaling:.2f}")
        if self.index is not None:
            components = OPTIONS.model.components.current
            getattr(components[self.index].params, self.name).value = value / self.scaling

            # TODO: Make this somehow somwhere else so that one slider controls all
            if self.name in ["cinc", "pa"] and OPTIONS.display.coplanar:
                for component in components.values():
                    getattr(component.params, self.name).value = value / self.scaling

        self.parent.parent.display_model()

    def updateSliderFromLineEdit(self):
        """Updates the slider with the new value."""
        value = round(float(self.lineEdit.text()), 2)
        self.slider.setValue(int(value * self.scaling))
        self.lineEdit.setText(f"{value:.2f}")
