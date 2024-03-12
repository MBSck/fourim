from PySide6.QtWidgets import QWidget
import matplotlib
import numpy as np

matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class LivePlotCanvas1D(FigureCanvasQTAgg):
    """

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

    def __init__(self, parent: QWidget = None,
                 width: int = 5, height: int = 4, dpi: int = 100) -> None:
        """The class constructor."""
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(LivePlotCanvas, self).__init__(fig)
        self.setParent(parent)

        self.x = np.linspace(0, 2*np.pi, 100)
        self.y = np.sin(self.x)

    def update_plot(self):
        """Updates the plot with the new model."""
        self.y = np.roll(self.y, -1)
        self.axes.cla()
        self.axes.plot(self.x, self.y)
        self.draw()


class LivePlotCanvas2D(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(LivePlotCanvas, self).__init__(fig)
        self.setParent(parent)

        self.x = np.linspace(0, 2*np.pi, 100)
        self.y = np.sin(self.x)

    def update_plot(self):
        self.y = np.roll(self.y, -1)
        self.axes.cla()  # Clear the canvas.
        self.axes.plot(self.x, self.y)
        self.draw()
