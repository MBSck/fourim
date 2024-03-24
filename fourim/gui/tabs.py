from typing import Optional

import astropy.units as u
import numpy as np
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, \
    QLabel, QComboBox, QHBoxLayout, QRadioButton
from ppdmod.utils import compute_effective_baselines, compute_vis

from .plot import MplCanvas
from .slider import ScrollBar
from ..options import OPTIONS
from ..utils import set_active_model


# TODO: Add setting for wavelength (maybe slider for wavelength range)
# TODO: Think about chaching the models if parameters are changed for wavelength playing
# TODO: Add setting to choose between x, y and x and sep
class SettingsTab(QWidget):
    """The settings tab for the GUI."""

    def __init__(self, parent: Optional[QWidget] = None,
                 plots: Optional[QWidget] = None) -> None:
        """The class's initialiser."""
        super().__init__(parent)
        layout = QVBoxLayout()
        self.plots = plots
        self.setLayout(layout)

        title_model = QLabel("Model:")
        self.model = QComboBox()
        for model in OPTIONS.model.avail:
            self.model.addItem(model)

        self.model.setCurrentIndex(0)
        self.selectedOption = self.model.currentText()
        self.model.currentIndexChanged.connect(lambda: self.change_model())
        layout.addWidget(title_model)
        layout.addWidget(self.model)

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
        layout.addWidget(title_dim)
        layout.addLayout(hLayout)

    def change_model(self) -> None:
        """Slot for model change."""
        OPTIONS.model.selected = self.model.currentText()
        set_active_model()
        self.plots.scroll_bar.update_scrollbar()
        self.plots.display_model()

    def toggle_dimension(self) -> None:
        """Slot for radio buttons toggled."""
        if self.one_dim_radio.isChecked():
            OPTIONS.display.one_dimensional = True
        elif self.two_dim_radio.isChecked():
            OPTIONS.display.one_dimensional = False
        self.plots.display_model()


class PlotTab(QWidget):
    """The plot tab for the GUI."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """The class's initialiser."""
        super().__init__(parent)
        layout = QGridLayout()

        self.canvas_left = MplCanvas(self, width=5, height=4)
        self.canvas_middle = MplCanvas(self, width=5, height=4)
        self.canvas_right = MplCanvas(self, width=5, height=4)
        self.scroll_bar = ScrollBar(self)
        layout.addWidget(self.canvas_left, 0, 0)
        layout.addWidget(self.canvas_middle, 0, 1)
        layout.addWidget(self.canvas_right, 0, 2)
        layout.addWidget(self.scroll_bar, 1, 0, 1, 3)

        layout.setRowStretch(0, 2)
        layout.setRowStretch(1, 1)

        self.setLayout(layout)
        self.display_model()

    # TODO: Make the 2D plots resize automatically, for bigger radii or model sizes
    def display_model(self):
        """Displays the model in the plot."""
        model, wl = OPTIONS.model.active, OPTIONS.model.wl
        pixel_size = OPTIONS.model.pixel_size

        if OPTIONS.display.one_dimensional:
            dim1d = OPTIONS.model.one_dim

            ucoord = np.linspace(0, 100, dim1d)*u.m
            baselines, _ = compute_effective_baselines(
                    ucoord, ucoord, model.inc.value, model.pa.value)

            complex_vis = model.compute_complex_vis(ucoord, ucoord, wl)[0][0]
            vis, phases = compute_vis(complex_vis), np.angle(complex_vis, deg=True)
            image = model.compute_image(OPTIONS.model.two_dim, pixel_size, wl)[0].value
            max_im = (OPTIONS.model.two_dim/2*pixel_size).value

            self.canvas_left.update_plot(image, title="Image", vlims=[0, 1],
                                         extent=[-max_im, max_im, -max_im, max_im],
                                         xlabel=r"$\alpha$ (mas)", ylabel=r"$\delta$ (mas)")
            self.canvas_middle.update_plot(baselines.value, vis, ylims=[-0.1, 1.1],
                                           title="Visibility", ylabel="Visibility (Normalised)")
            self.canvas_right.update_plot(baselines.value, phases, ylims=[-185, 185],
                                          title="Phase", ylabel="Phase (Degrees)")
        else:
            # fourier = compute_vis(jnp.fft.fftshift(jnp.fft.fft2(jnp.fft.fftshift(image))))
            # self.canvas_right.update_plot(fourier)
            ...
