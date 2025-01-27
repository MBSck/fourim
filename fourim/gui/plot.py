from typing import List, Optional

import astropy.units as u
import matplotlib
import matplotlib.lines as mlines
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

matplotlib.use("Qt5Agg")

from PySide6.QtWidgets import QWidget, QGridLayout

from ..backend.options import OPTIONS
from ..backend.utils import compute_effective_baselines, get_param_value
from .scrollbar import ScrollBar


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
        dim1d, dim2d = OPTIONS.model.one_dim, OPTIONS.model.two_dim

        if OPTIONS.display.one_dimensional:
            ucoord = np.linspace(0, 150, dim1d) * u.m
            # TODO: Make this for each component individually
            spf, psi = compute_effective_baselines(
                ucoord,
                ucoord,
                get_param_value(components[0].params.cinc),
                get_param_value(components[0].params.pa),
            )
            spf_wl = (spf / wl.to(u.m)).value / u.rad

            complex_vis, image = [], []
            for component in components.values():
                complex_vis.append(component.vis(spf_wl, 0, component.params))
                # img = component.image(dim2d, pixel_size, wl)
                # img /= img.max()
                # image.append(img)

            vis = np.sum(complex_vis, axis=0)
            vis_label = "Visibility"

            # max_im = (dim2d / 2 * pixel_size).value
            # self.canvas_left.update_plot(
            #     image,
            #     title="Image",
            #     vlims=[0, 1],
            #     extent=[-max_im, max_im, -max_im, max_im],
            #     xlabel=r"$\alpha$ (mas)",
            #     ylabel=r"$\delta$ (mas)",
            # )
            self.canvas_middle.update_plot(
                spf.value,
                vis,
                ylims=[-0.1, 1.1],
                title=r"$V^2$ (a.u.)",
            )
            # self.canvas_right.update_plot(
            #     baselines.value, phases, ylims=[-185, 185], title="Phase (Degrees)"
            # )

            # if self.file_manager.files:
            #     for readout in self.file_manager.files.values():
            #         vis = getattr(readout, output)
            #         # baselines, _ = compute_effective_baselines(
            #         #         vis.ucoord, vis.ucoord,
            #         #         components[0].inc.value, components[0].pa.value)
            #         value = readout.get_data_for_wavelength(
            #             wl, output, "value"
            #         ).flatten()
            #         err = readout.get_data_for_wavelength(wl, output, "err").flatten()
            #         self.canvas_middle.overplot(baselines, value, yerr=err)
            #
            #         t3 = readout.t3
            #         # baselines, _ = compute_effective_baselines(
            #         #         t3.u123coord, t3.u123coord,
            #         #         components[0].inc.value, components[0].pa.value,
            #         #         longest=True)
            #
            #         value = readout.get_data_for_wavelength(wl, "t3", "value").flatten()
            #         err = readout.get_data_for_wavelength(wl, "t3", "err").flatten()
            #         self.canvas_right.overplot(baselines, value, yerr=err)
            #
            #         complex_vis = np.sum(
            #             [
            #                 comp.compute_complex_vis(t3.u123coord, t3.v123coord, wl)
            #                 for comp in components.values()
            #             ],
            #             axis=0,
            #         )
            #         # closure_phase = compute_t3(complex_vis)
            #         self.canvas_right.overplot(baselines, closure_phase)
            #         self.canvas_right.add_legend()

        # TODO: Think about using the real fouriertransform to makes these images quickly
        # use Jax and the symmetries of Fourier transforms.
        else:
            # fourier = compute_vis(jnp.fft.fftshift(jnp.fft.fft2(jnp.fft.fftshift(image))))
            # self.canvas_right.update_plot(fourier)
            ...
