from typing import Optional

import astropy.units as u
from PySide6.QtWidgets import (
    QGridLayout,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from ..backend.options import OPTIONS
from .slider import SliderWithInput


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
        OPTIONS.model.wl = [value / self.wavelength.scaling] * u.um
        self.parent.display_model()

    def update_scrollbar(self):
        """Updates the scroll bar with new sliders
        depending on the model used."""
        if self.wavelength is not None:
            self.sliders_grid.removeWidget(self.wavelength)
            self.wavelength.deleteLater()

        # self.wavelength = SliderWithInput(
        #     self,
        #     "Wavelength",
        #     "µm",
        #     1,
        #     100,
        #     OPTIONS.model.wl.value[0],
        #     update_function=self.wavelength_update,
        # )
        # self.sliders_grid.addWidget(self.wavelength, 1, 0)

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
            for param in vars(component.params).values():
                slider = SliderWithInput(self, param, index=index)
                self.sliders.append(slider)
                self.sliders_grid.addWidget(slider)

                slider.slider.setFixedWidth(200)
                slider.lineEdit.setFixedWidth(80)

                self.sliders_grid.addWidget(slider, row, col)
                col += 1
                if col >= sliders_per_row:
                    col, row = 0, row + 1
            row += 1
            self.names.append(name)
