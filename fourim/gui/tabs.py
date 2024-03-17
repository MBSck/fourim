from typing import Optional

import astropy.units as u
import numpy as np
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, \
    QGridLayout, QRadioButton, QHBoxLayout, QComboBox
from ppdmod.utils import compute_effective_baselines, compute_vis

from .plot import MplCanvas
from .slider import ScrollBar
from ..options import OPTIONS
from ..utils import set_active_model


# TODO: Add setting for wavelength (maybe slider for wavelength range)
# TODO: Think about chaching the models if parameters are changed for wavelength playing
# TODO: Add setting to choose between x, y and x and sep
# TODO: Make settings for phases and amplitude
class SettingsTab(QWidget):

    def __init__(self, parent: Optional[QWidget] = None,
                 plots: Optional[QWidget] = None) -> None:
        """The class's initialiser."""
        super().__init__(parent)
        layout = QVBoxLayout()
        self.plots = plots

        title_model = QLabel("Model:")
        self.model = QComboBox()
        for model in OPTIONS.model.avail:
            self.model.addItem(model)

        self.model.setCurrentIndex(0)
        self.selectedOption = self.model.currentText()
        self.model.currentIndexChanged.connect(lambda: self.change_model())
        layout.addWidget(title_model)
        layout.addWidget(self.model)

        title_dim = QLabel("Plot Dimensionality:")
        hLayout = QHBoxLayout()

        self.one_dim_radio = QRadioButton("1D")
        self.one_dim_radio.toggled.connect(self.toggle_dimension)
        self.one_dim_radio.setChecked(OPTIONS.display.one_dimensional)
        hLayout.addWidget(self.one_dim_radio)

        self.two_dim_radio = QRadioButton("2D")
        self.two_dim_radio.toggled.connect(self.toggle_dimension)
        self.two_dim_radio.setChecked(not OPTIONS.display.one_dimensional)
        hLayout.addWidget(self.two_dim_radio)

        layout.addWidget(title_dim)
        layout.addLayout(hLayout)
        self.setLayout(layout)

    def toggle_dimension(self) -> None:
        """Slot for radio buttons toggled."""
        if self.one_dim_radio.isChecked():
            OPTIONS.display.one_dimensional = True
        elif self.two_dim_radio.isChecked():
            OPTIONS.display.one_dimensional = False
        self.plots.display_model()

    def change_model(self) -> None:
        """Slot for model change."""
        OPTIONS.model.selected = self.model.currentText()
        set_active_model()
        self.plots.scroll_bar.update_scrollbar()
        self.plots.display_model()


class PlotTab(QWidget):

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """The class's initialiser."""
        super().__init__(parent)
        layout = QGridLayout()

        self.canvas_left = MplCanvas(self, width=5, height=4, dpi=100)
        self.canvas_right = MplCanvas(self, width=5, height=4, dpi=100)
        self.scroll_bar = ScrollBar(self)
        layout.addWidget(self.canvas_left, 0, 0)
        layout.addWidget(self.canvas_right, 0, 1)
        layout.addWidget(self.scroll_bar, 0, 2)
        self.setLayout(layout)
        self.display_model()

    def display_model(self):
        model = OPTIONS.model.active
        dim, wl = OPTIONS.model.dim, OPTIONS.model.wl
        if OPTIONS.display.one_dimensional:
            ucoord = np.linspace(0, 100)*u.m
            fourier = model.compute_complex_vis(ucoord, ucoord, wl)
            vis = compute_vis(fourier)[0][0]
            eff_baselines, _ = compute_effective_baselines(
                    ucoord, ucoord, model.inc.value, model.pa.value)
            self.canvas_left.update_plot(eff_baselines.value, vis)
            # self.canvas_right.update_plot([])
        else:
            image = model.compute_image(dim, OPTIONS.model.pixel_size, wl)
            # TODO: Make this better and changeable
            ucoord = np.linspace(0, 100)*u.m
            ucoord, vcoord = np.meshgrid(ucoord, ucoord)
            # fourier = compute_vis(model.compute_complex_vis(ucoord, vcoord, wl))
            self.canvas_left.update_plot(image[0])
            # self.canvas_right.update_plot(fourier[0])
