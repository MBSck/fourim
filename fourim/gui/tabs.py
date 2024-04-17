from typing import Optional

import astropy.units as u
import numpy as np
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, \
    QLabel, QComboBox, QHBoxLayout, QRadioButton, QPushButton, QListWidget
from ppdmod.utils import compute_effective_baselines, compute_vis

from .plot import MplCanvas
from .slider import ScrollBar
from ..options import OPTIONS


# TODO: Add setting for wavelength (maybe slider for wavelength range)
# TODO: Think about chaching the models if parameters are changed for wavelength playing
# TODO: Make the 2D plots resize automatically, for bigger radii or model sizes
# TODO: Add setting to choose between x, y and x and sep
# TODO: Add file loading and overplotting
# TODO: Add switch to baseline view (wavelengths on x-axis?) Or rather 
# multiple wavelengths in one plot
# Add logarithmic representation in image space
class SettingsTab(QWidget):
    """The settings tab for the GUI."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """The class's initialiser."""
        super().__init__(parent)
        layout = QVBoxLayout()
        self.plots = parent.plot_tab
        self.component_manager = parent.component_manager
        self.setLayout(layout)

        label_model = QLabel("Model:")
        self.model_combo = QComboBox()
        self.model_list = QListWidget()
        self.model_combo.addItems(OPTIONS.model.components.avail)

        self.add_button = QPushButton("+")
        self.remove_button = QPushButton("-")
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.remove_button)

        self.model_combo.setCurrentIndex(0)
        self.selectedOption = self.model_combo.currentText()
        layout.addWidget(label_model)
        layout.addWidget(self.model_combo)
        layout.addLayout(button_layout)
        layout.addWidget(self.model_list)

        self.model_list.addItem(self.model_combo.currentText())
        self.add_button.clicked.connect(self.add_model)
        self.remove_button.clicked.connect(self.remove_model)

        title_dim = QLabel("Plot Dimension:")
        hLayout_dim = QHBoxLayout()

        self.one_dim_radio = QRadioButton("1D")
        self.one_dim_radio.toggled.connect(self.toggle_dimension)
        self.one_dim_radio.setChecked(OPTIONS.display.one_dimensional)
        hLayout_dim.addWidget(self.one_dim_radio)

        self.two_dim_radio = QRadioButton("2D")
        self.two_dim_radio.toggled.connect(self.toggle_dimension)
        self.two_dim_radio.setChecked(not OPTIONS.display.one_dimensional)
        hLayout_dim.addWidget(self.two_dim_radio)
        layout.addWidget(title_dim)
        layout.addLayout(hLayout_dim)

        title_model_output = QLabel("Model Ouput:")
        hLayout_model_output = QHBoxLayout()

        self.vis_radio = QRadioButton("Visibilities (Vis)")
        self.vis_radio.toggled.connect(self.toggle_output)
        self.vis_radio.setChecked(OPTIONS.display.output == "vis")
        hLayout_model_output.addWidget(self.vis_radio)

        self.vis2_radio = QRadioButton("Squared Visibilities (Vis2)")
        self.vis2_radio.toggled.connect(self.toggle_output)
        self.vis2_radio.setChecked(OPTIONS.display.output == "vis2")
        hLayout_model_output.addWidget(self.vis2_radio)
        layout.addWidget(title_model_output)
        layout.addLayout(hLayout_model_output)

        title_coplanar = QLabel("Coplanar (shared orientation):")
        hLayout_coplanar = QHBoxLayout()

        self.coplanar_true_radio = QRadioButton("Yes")
        self.coplanar_true_radio.toggled.connect(self.toggle_coplanar)
        self.coplanar_true_radio.setChecked(OPTIONS.display.coplanar)
        hLayout_coplanar.addWidget(self.coplanar_true_radio)

        self.coplanar_false_radio = QRadioButton("No")
        self.coplanar_false_radio.toggled.connect(self.toggle_coplanar)
        self.coplanar_false_radio.setChecked(not OPTIONS.display.coplanar)
        hLayout_coplanar.addWidget(self.coplanar_false_radio)
        layout.addWidget(title_coplanar)
        layout.addLayout(hLayout_coplanar)
        
    def add_model(self) -> None:
        """Adds the model from the drop down selection to the model list."""
        current_component = self.model_combo.currentText()
        self.model_list.addItem(current_component)
        self.component_manager.add_component(current_component)
        self.plots.scroll_bar.update_scrollbar()
        self.plots.display_model()

    def remove_model(self) -> None:
        """Removes the model from the drop down selection to the model list."""
        list_items = self.model_list.selectedItems()
        if not list_items:
            return

        for item in list_items:
            index = self.model_list.row(item)
            self.component_manager.remove_component(index)
            self.model_list.takeItem(index)

        self.plots.scroll_bar.update_scrollbar()
        self.plots.display_model()

    def toggle_dimension(self) -> None:
        """Slot for radio buttons toggled."""
        if self.one_dim_radio.isChecked():
            OPTIONS.display.one_dimensional = True
        elif self.two_dim_radio.isChecked():
            OPTIONS.display.one_dimensional = False
        self.plots.display_model()

    def toggle_output(self) -> None:
        """Slot for radio buttons toggled."""
        if self.vis_radio.isChecked():
            OPTIONS.display.output = "vis"
        elif self.vis2_radio.isChecked():
            OPTIONS.display.output = "vis2"
        self.plots.display_model()

    def toggle_coplanar(self) -> None:
        """Slot for radio buttons toggled."""
        if self.coplanar_true_radio.isChecked():
            OPTIONS.display.coplanar = True
        elif self.coplanar_false_radio.isChecked():
            OPTIONS.display.coplanar = False
        self.plots.display_model()


# TODO: Add support for different scalings of the 1D baseline axis
# TODO: Add support to overplot the different VLTI and ALMA configurations
# TODO: Add save and load functionalities to models
class PlotTab(QWidget):
    """The plot tab for the GUI."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """The class's initialiser."""
        super().__init__(parent)
        self.component_manager = parent.component_manager

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

    def display_model(self):
        """Displays the model in the plot."""
        components = self.component_manager.components
        wl, pixel_size = OPTIONS.model.wl, OPTIONS.model.pixel_size
        dim1d, dim2d = OPTIONS.model.one_dim, OPTIONS.model.two_dim

        # TODO: Include here also the calculation of T3 from the model and show
        # the ones from the files
        if OPTIONS.display.one_dimensional:
            ucoord = np.linspace(0, 100, dim1d)*u.m
            # TODO: Make it so that position angle and so can be NOT shared
            baselines, _ = compute_effective_baselines(
                    ucoord, ucoord, components[0].inc.value, components[0].pa.value)

            complex_vis = np.sum([comp.compute_complex_vis(ucoord, ucoord, wl)[0][0]
                                  for comp in components.values()], axis=0)
            vis, phases = compute_vis(complex_vis), np.angle(complex_vis, deg=True)
            image = np.sum([comp.compute_image(dim2d, pixel_size, wl)[0].value
                            for comp in components.values()], axis=0)
            image /= image.max()
            max_im = (dim2d/2*pixel_size).value

            if OPTIONS.display.output == "vis2":
                vis = vis**2
                vis_label = "Squared Visibility"
            else:
                vis_label = "Visibility"

            self.canvas_left.update_plot(image, title="Image", vlims=[0, 1],
                                         extent=[-max_im, max_im, -max_im, max_im],
                                         xlabel=r"$\alpha$ (mas)", ylabel=r"$\delta$ (mas)")
            self.canvas_middle.update_plot(baselines.value, vis, ylims=[-0.1, 1.1],
                                           title=f"{vis_label} (Normalised)")
            self.canvas_right.update_plot(baselines.value, phases, ylims=[-185, 185],
                                          title="Phase (Degrees)")
        # TODO: Think about using the real fouriertransform to makes these images quickly
        else:
            # fourier = compute_vis(jnp.fft.fftshift(jnp.fft.fft2(jnp.fft.fftshift(image))))
            # self.canvas_right.update_plot(fourier)
            ...
