from collections.abc import Callable
from typing import Optional

import astropy.units as u
import numpy as np
from PySide6.QtWidgets import QWidget, QHBoxLayout, QSlider, \
    QLineEdit, QLabel, QScrollArea, QVBoxLayout, QGridLayout
from PySide6.QtCore import Qt

from ..backend.options import OPTIONS


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
    component_manager : ComponentManager
        The component manager.
    scaling : float
        The scaling factor.
    name : str
        The name of the parameter.
    label : QLabel
        The label of the slider.
    unit : QLabel
        The unit of the parameter.
    slider : QSlider
        The slider.
    lineEdit : QLineEdit
        The input field.
    """

    def __init__(self, parent: QWidget,
                 name: str, unit: str,
                 min_value: float, max_value: float,
                 initial_value: Optional[float],
                 update_function: Optional[Callable] = None,
                 index: Optional[int] = None) -> None:
        """The class's initialiser."""
        super().__init__()
        self.parent, self.index = parent, index
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
        self.slider.valueChanged.connect(
                self.updateLineEdit if update_function is None else update_function)
        
        self.lineEdit = QLineEdit(f"{initial_value:.2f}")
        self.lineEdit.returnPressed.connect(self.updateSliderFromLineEdit)
        
        slider_layout.addWidget(self.slider)
        slider_layout.addWidget(self.lineEdit)
        main_layout.addLayout(slider_layout)
        self.setLayout(main_layout)
        
    def updateLineEdit(self, value: float):
        """Updates the line edit with the new value."""
        self.lineEdit.setText(f"{value/self.scaling:.2f}")
        if self.index is not None:
            component = self.component_manager.get_component(self.index)
            getattr(component, self.name).value = value/self.scaling

            # TODO: Make this somehow somwhere else so that one slider controls all
            if self.name in ["inc", "pa"] and OPTIONS.display.coplanar:
                components = self.component_manager.get_all_components()
                for comp in components:
                    getattr(comp, self.name).value = value/self.scaling

        self.parent.parent.display_model()
        
    def updateSliderFromLineEdit(self):
        """Updates the slider with the new value."""
        value = round(float(self.lineEdit.text()), 2)
        self.slider.setValue(int(value*self.scaling))
        self.lineEdit.setText(f"{value:.2f}")


class ScrollBar(QWidget):
    """A scroll bar widget that encompasses all the parameters.

    Parameters
    ----------
    parent : QWidget
        The parent widget.

    Attributes
    ----------
    parent : QWidget
        The parent widget.
    component_manager : ComponentManager
        The component manager.
    wavelength : SliderWithInput
        The wavelength slider.
    names : list of QLabel
        The list of component names.
    sliders_grid : QGridLayout
        The grid layout for the sliders.
    sliders_container : QWidget
        The container for the sliders.
    sliders : list of SliderWithInput
        The list of sliders.
    main_layout : QVBoxLayout
        The main layout.
    scroll_area : QScrollArea
        The scroll area.
    main_layout : QVBoxLayout
        The main layout.
    """

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """The class constructor."""
        super().__init__(parent)
        self.parent = parent

        self.wavelength, self.names = None, []
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

    def wavelength_update(self, value: float):
        """Updates the line edit with the new value."""
        self.wavelength.lineEdit.setText(f"{value/self.wavelength.scaling:.2f}")
        OPTIONS.model.wl = [value/self.wavelength.scaling]*u.um
        self.parent.display_model()

    def update_scrollbar(self):
        """Updates the scroll bar with new sliders
        depending on the model used."""
        if self.wavelength is not None:
            self.sliders_grid.removeWidget(self.wavelength)
            self.wavelength.deleteLater()

        self.wavelength = SliderWithInput(
                self, "Wavelength", "µm", 1, 100,
                OPTIONS.model.wl.value[0],
                update_function=self.wavelength_update)
        self.sliders_grid.addWidget(self.wavelength, 1, 0)

        if self.names:
            for name in self.names:
                self.sliders_grid.removeWidget(name)
                name.deleteLater()
            self.names = []

        if self.sliders:
            for slider in self.sliders:
                self.sliders_grid.removeWidget(slider)
                slider.deleteLater()
            self.sliders = []

        row = 2
        for index, component in OPTIONS.model.components.current.items():
            name = QLabel(f"{component.name}:")
            self.sliders_grid.addWidget(name, row, 0)
            row += 1

            row, col, sliders_per_row = row, 0, 4
            for param, value in vars(component.params).items():
                slider = SliderWithInput(
                        self, param, "",
                        0, 10, value, index=index)
                self.sliders.append(slider)
                self.sliders_grid.addWidget(slider)

                slider.slider.setFixedWidth(200)
                slider.lineEdit.setFixedWidth(80)

                self.sliders_grid.addWidget(slider, row, col)
                col += 1
                if col >= sliders_per_row:
                    col, row = 0, row+1
            row += 1
            self.names.append(name)
