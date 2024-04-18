from typing import List, Optional

import matplotlib
import matplotlib.lines as mlines
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

matplotlib.use('Qt5Agg')

from PySide6.QtWidgets import QWidget
from ppdmod.options import plot


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

    def __init__(self, parent: QWidget, width: int,
                 height: int, dpi: Optional[int] = 100) -> None:
        """The class's initialiser."""
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)
        self.show()

    def update_plot(self, xdata: np.ndarray,
                    ydata: Optional[np.ndarray] = None,
                    ylims: Optional[List[float]] = None,
                    extent: Optional[List[float]] = None,
                    title: Optional[str] = None,
                    vlims: Optional[List[float]] = [None, None],
                    xlabel: Optional[str] = None,
                    ylabel: Optional[str] = None) -> None:
        """Update the plot with the new model images."""
        self.axes.cla()
        if ydata is not None:
            self.axes.plot(xdata, ydata)
            self.axes.set_ylim(ylims)
            self.axes.set_xlabel(r"$B_{\mathrm{eff}}$ $\left(\mathrm{M}\lambda\right)$")
        else:
            self.axes.imshow(xdata, extent=extent,
                             vmin=vlims[0], vmax=vlims[1])
            self.axes.set_xlabel(xlabel)
        self.axes.set_ylabel(ylabel)
        self.axes.set_title(title)
        self.draw()

    # TODO: Add Better color support
    def overplot(self, xdata: np.ndarray,
                 ydata: np.ndarray,
                 yerr: Optional[np.ndarray] = None,
                 label: Optional[str] = None) -> None:
        """Overplot the data."""
        if yerr is not None:
            self.axes.errorbar(xdata, ydata, yerr,
                               label=label, fmt="o", **vars(plot.errorbar))
        else:
            scatter_kwargs = plot.scatter
            scatter_kwargs.color = None
            self.axes.scatter(xdata, ydata, label=label,
                              marker="X", **vars(scatter_kwargs))
        self.draw()

    def add_legend(self) -> None:
        """Add a legend to the plot."""
        dot_label = mlines.Line2D([], [], color="k", marker="o",
                                  linestyle="None", label="Data", alpha=0.6)
        x_label = mlines.Line2D([], [], color="k", marker="X",
                                linestyle="None", label="Model")
        self.axes.legend(handles=[dot_label, x_label])
        self.draw()
