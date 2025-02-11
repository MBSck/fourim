from typing import List, Optional

import matplotlib
import matplotlib.lines as mlines
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

matplotlib.use("Qt5Agg")

from PySide6.QtWidgets import QGridLayout, QWidget

from ..backend.compute import (
    compute_amplitude,
    compute_complex_vis,
    compute_image,
    compute_phase,
    convert_coords_to_polar,
)
from ..config.options import OPTIONS
from .scrollbar import ScrollBar

# TODO: Make it so this setting can be chosen by user
plt.style.use("dark_background")


class MplCanvas(FigureCanvasQTAgg):
    """The base class for a live updating.

    Parameters
    ----------
    parent : QWidget
        The parent widget.
    width : int
        The width of the plot.
    height : int
        The height of the plot.
    dpi : int
        The dots per inch of the plot.
    """

    def __init__(
        self, parent: QWidget, width: int, height: int, dpi: Optional[int] = 100
    ) -> None:
        """The class's initialiser."""
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)
        self.show()

    def update_plot(
        self,
        xdata: np.ndarray,
        ydata: Optional[np.ndarray] = None,
        ylims: Optional[List[float]] = None,
        extent: Optional[List[float]] = None,
        title: Optional[str] = None,
        vlims: Optional[List[float]] = [None, None],
        xlabel: Optional[str] = None,
        ylabel: Optional[str] = None,
    ) -> None:
        """Update the plot with the new model images."""
        self.axes.cla()
        if ydata is not None:
            self.axes.plot(xdata, ydata)
            self.axes.set_ylim(ylims)
            self.axes.set_xlabel(r"$B_{\mathrm{eff}}$ $\left(\mathrm{M}\lambda\right)$")
        else:
            self.axes.imshow(xdata, extent=extent, vmin=vlims[0], vmax=vlims[1])
            self.axes.set_xlabel(xlabel)
        self.axes.set_ylabel(ylabel)
        self.axes.set_title(title)
        self.draw()

    # TODO: Add Better color support
    def overplot(
        self,
        xdata: np.ndarray,
        ydata: np.ndarray,
        yerr: Optional[np.ndarray] = None,
        label: Optional[str] = None,
    ) -> None:
        """Overplot the data."""
        if yerr is not None:
            self.axes.errorbar(xdata, ydata, yerr, label=label, fmt="o")
        else:
            self.axes.scatter(xdata, ydata, label=label, marker="X")
        self.draw()

    def add_legend(self) -> None:
        """Add a legend to the plot."""
        dot_label = mlines.Line2D(
            [], [], color="k", marker="o", linestyle="None", label="T3 Data", alpha=0.6
        )
        x_label = mlines.Line2D(
            [], [], color="k", marker="X", linestyle="None", label="T3 Model"
        )
        self.axes.legend(handles=[dot_label, x_label])
        self.draw()


# TODO: Move plot tab to its own file
# TODO: Add support for different scalings of the 1D baseline axis
# TODO: Add support to overplot the different VLTI and ALMA configurations
# TODO: Add save and load functionalities to models
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

    # TODO: Add legend at some point
    def display_model(self):
        """Displays the model in the plot."""
        components = OPTIONS.model.components.current
        wl, pixel_size = OPTIONS.model.wl, OPTIONS.model.pixel_size
        dim, max_im = OPTIONS.model.dim, OPTIONS.model.dim / 2 * pixel_size

        x = np.linspace(-0.5, 0.5, dim, endpoint=False) * max_im * 2
        xx, yy = np.meshgrid(x, x)
        self.canvas_left.update_plot(
            compute_image(components, xx, yy),
            title="Model Image",
            vlims=[0, 1],
            extent=[-max_im, max_im, -max_im, max_im],
            xlabel=r"$\alpha$ (mas)",
            ylabel=r"$\delta$ (mas)",
        )

        ucoord = np.linspace(0, 150, dim * 2)
        spf, _ = convert_coords_to_polar(ucoord, ucoord)
        complex_vis = compute_complex_vis(components, ucoord, wl)
        self.canvas_middle.update_plot(
            spf,
            compute_amplitude(complex_vis),
            ylims=[-0.1, 1.1],
            ylabel=OPTIONS.settings.display.label,
            title=r"Amplitudes",
        )
        self.canvas_right.update_plot(
            spf,
            compute_phase(complex_vis),
            ylims=[-185, 185],
            ylabel=r"$\phi$ ($^\circ$)",
            title="Phases",
        )
