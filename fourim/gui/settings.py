from pathlib import Path
from typing import Optional

from PySide6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QRadioButton,
    QVBoxLayout,
    QWidget,
)

from ..backend.components import make_component
from ..config.options import OPTIONS


# TODO: Move settings tab to its own file
# TODO: Think about chaching the models if parameters are changed for wavelength playing
# TODO: Make the 2D plots resize automatically, for bigger radii or model sizes
# TODO: Add setting to choose between x, y and x and sep
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
        self.setLayout(layout)

        label_model = QLabel("Model:")
        self.model_combo = QComboBox()
        self.model_list = QListWidget()

        available_components = list(vars(OPTIONS.model.components.avail).keys())
        self.model_combo.addItems(available_components)

        self.add_button = QPushButton("+")
        self.remove_button = QPushButton("-")
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.remove_button)

        self.model_combo.setCurrentIndex(0)
        layout.addWidget(label_model)
        layout.addWidget(self.model_combo)
        layout.addLayout(button_layout)
        layout.addWidget(self.model_list)

        self.model_list.addItem(OPTIONS.model.components.init)
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

        title_file = QLabel("Data Files:")
        self.open_file_button = QPushButton("Open (.fits)-file")
        self.open_file_button.clicked.connect(self.open_file_dialog)
        self.file_widget = QListWidget()
        layout.addWidget(title_file)
        layout.addWidget(self.open_file_button)
        layout.addWidget(self.file_widget)

    def add_model(self) -> None:
        """Adds the model from the drop down selection to the model list."""
        current_component = self.model_combo.currentText()
        self.model_list.addItem(current_component)
        OPTIONS.model.components.current[len(OPTIONS.model.components.current) + 1] = (
            make_component(current_component)
        )
        self.plots.scroll_bar.update_scrollbar()
        self.plots.display_model()

    def remove_model(self) -> None:
        """Removes the model from the drop down selection to the model list."""
        list_items = self.model_list.selectedItems()
        if not list_items:
            return

        for item in list_items:
            index = self.model_list.row(item)
            del OPTIONS.model.components.current[index]
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

    def open_file_dialog(self):
        """Open a file dialog to select files to open.

        Allows for multiple file opening.
        """
        file_names, _ = QFileDialog.getOpenFileNames(
            self, "Open File", "", "All Files (*);;Text Files (*.txt)"
        )

        for file_name in file_names:
            self.add_file_to_list(file_name)

    def add_file_to_list(self, file_name: Path):
        """Add a file to the list widget."""
        text = Path(file_name)
        item = QListWidgetItem(self.file_widget)
        item.setText(text.name)

        widget = QWidget()
        layout = QHBoxLayout(widget)
        close_button = QPushButton("X")
        close_button.clicked.connect(lambda: self.remove_file(item))
        layout.addStretch(1)
        layout.addWidget(close_button)
        layout.addStretch()

        widget.setLayout(layout)
        item.setSizeHint(widget.sizeHint())
        self.file_widget.addItem(item)
        self.file_widget.setItemWidget(item, widget)
        self.file_manager.add_file(file_name)
        self.plots.display_model()

    def remove_file(self, item):
        """Remove a file from the list widget."""
        row = self.file_widget.row(item)
        self.file_manager.remove_file(item.text())
        self.file_widget.takeItem(row)
        self.plots.display_model()
