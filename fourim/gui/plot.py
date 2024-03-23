from typing import List, Optional

import matplotlib
import numpy as np

matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PySide6.QtWidgets import QWidget

from ..options import OPTIONS


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
                 height: int, dpi: Optional[int] = 300) -> None:
        """The class's initialiser."""
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)
        self.show()

    def update_plot(self, xdata: np.ndarray,
                    ydata: Optional[np.ndarray] = None,
                    ylims: Optional[List[float]] = None,
                    title: Optional[str] = None,
                    ylabel: Optional[str] = None) -> None:
        """Update the plot with the new model images."""
        self.axes.cla()
        if OPTIONS.display.one_dimensional:
            self.axes.plot(xdata, ydata)
            self.axes.set_ylim(ylims)
            self.axes.set_ylabel(ylabel)
            self.axes.set_xlabel(r"$B_{\mathrm{eff}}$ $\left(M\lambda\right)$")
        else:
            self.axes.imshow(xdata)
        self.axes.set_title(title)
        self.draw()

