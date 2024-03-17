from typing import Optional

import matplotlib
import numpy as np

matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PySide6.QtWidgets import QWidget


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
                 height: int, dpi: int = 300) -> None:
        """The class's initialiser."""
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)
        self.show()

    def update_plot(self, xdata: np.ndarray,
                    ydata: Optional[np.ndarray] = None) -> None:
        """Update the plot with the new model images."""
        self.axes.cla()
        if ydata is None:
            self.axes.imshow(xdata)
        else:
            self.axes.plot(xdata, ydata)
            self.axes.set_ylim([-0.1, 1.1])
        self.draw()

