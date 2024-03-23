from typing import Optional

import astropy.units as u
import numpy as np
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout
from ppdmod.utils import compute_effective_baselines, compute_vis

from .plot import MplCanvas
from .slider import ScrollBar
from ..options import OPTIONS


# TODO: Add setting for wavelength (maybe slider for wavelength range)
# TODO: Think about chaching the models if parameters are changed for wavelength playing
# TODO: Add setting to choose between x, y and x and sep
# TODO: Make settings for phases and amplitude in the 2D implementation
class SettingsTab(QWidget):
    """The settings tab for the GUI."""

    def __init__(self, parent: Optional[QWidget] = None,
                 plots: Optional[QWidget] = None) -> None:
        """The class's initialiser."""
        super().__init__(parent)
        layout = QVBoxLayout()
        self.plots = plots
        self.setLayout(layout)


class PlotTab(QWidget):
    """The plot tab for the GUI."""

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
        """Displays the model in the plot."""
        model, wl = OPTIONS.model.active, OPTIONS.model.wl

        if OPTIONS.display.one_dimensional:
            dim = OPTIONS.model.one_dim
            ucoord = np.linspace(0, 100, dim)*u.m
            fourier = model.compute_complex_vis(ucoord, ucoord, wl)
            vis = compute_vis(fourier)[0][0]
            phases = np.angle(fourier, deg=True)[0][0]
            eff_baselines, _ = compute_effective_baselines(
                    ucoord, ucoord, model.inc.value, model.pa.value)
            self.canvas_left.update_plot(eff_baselines.value, vis, ylims=[-0.1, 1.1],
                                         title="Visibility", ylabel="Visibility (Normalised)")
            self.canvas_right.update_plot(eff_baselines.value, phases, ylims=[-185, 185],
                                          title="Phase", ylabel="Phase (Degrees)")
        else:
            dim = OPTIONS.model.two_dim
            image = model.compute_image(dim, OPTIONS.model.pixel_size, wl)
            # TODO: Make this better and changeable
            ucoord = np.linspace(0, 100, dim)*u.m
            ucoord, vcoord = np.meshgrid(ucoord, ucoord)
            # fourier = compute_vis(model.compute_complex_vis(ucoord, vcoord, wl))
            self.canvas_left.update_plot(image[0])
            # self.canvas_right.update_plot(fourier[0])
