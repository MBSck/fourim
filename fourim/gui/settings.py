# from pathlib import Path
from typing import Optional

from PySide6.QtWidgets import (
    QComboBox,
    # QFileDialog,
    QHBoxLayout,
    QLabel,
    QListWidget,
    # QListWidgetItem,
    QPushButton,
    QRadioButton,
    QVBoxLayout,
    QWidget,
)

from ..backend.components import make_component
from ..config.options import OPTIONS


# TODO: Add setting to choose between x, y and x and sep
# TODO: Add switch to baseline view (wavelengths on x-axis?) Or rather
# multiple wavelengths in one plot
class SettingsTab(QWidget):
    """The settings tab for the GUI."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """The class's initialiser."""
        super().__init__(parent)
        layout = QVBoxLayout()
        self.plots = parent.plot_tab
        self.setLayout(layout)

        # TODO: Move this as a setting to the main page
        title_model_output = QLabel("Amplitude:")
        hLayout_model_output = QHBoxLayout()

        self.vis_radio = QRadioButton("Visibility")
        self.vis_radio.toggled.connect(self.toggle_amplitude)
        self.vis_radio.setChecked(OPTIONS.settings.display.amplitude == "vis")
        hLayout_model_output.addWidget(self.vis_radio)

        self.vis2_radio = QRadioButton("Visibility squared")
        self.vis2_radio.toggled.connect(self.toggle_amplitude)
        self.vis2_radio.setChecked(OPTIONS.settings.display.amplitude == "vis2")
        hLayout_model_output.addWidget(self.vis2_radio)
        layout.addWidget(title_model_output)
        layout.addLayout(hLayout_model_output)

        # TODO: Move this to the main tab (as a openable dialog)
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

        # TODO: Reimplement the overplotting of files
        # title_file = QLabel("Data Files:")
        # self.open_file_button = QPushButton("Open (.fits)-file")
        # self.open_file_button.clicked.connect(self.open_file_dialog)
        # self.file_widget = QListWidget()
        # layout.addWidget(title_file)
        # layout.addWidget(self.open_file_button)
        # layout.addWidget(self.file_widget)

    def add_model(self) -> None:
        """Adds the model from the drop down selection to the model list."""
        current_component = self.model_combo.currentText()
        self.model_list.addItem(current_component)
        OPTIONS.model.components.current[self.model_combo.currentIndex()] = (
            make_component(current_component)
        )
        self.plots.scroll_bar.update_scrollbar()
        self.plots.display_model()

    def remove_model(self) -> None:
        """Removes the model from the drop down selection to the model list."""
        items = self.model_list.selectedItems()
        if not items:
            return

        item = items[0]
        index = self.model_list.row(item)
        self.model_list.takeItem(index)
        del OPTIONS.model.components.current[index]

        self.plots.scroll_bar.update_scrollbar()
        self.plots.display_model()

    def toggle_amplitude(self) -> None:
        """Slot for radio buttons toggled."""
        if self.vis_radio.isChecked():
            OPTIONS.settings.display.amplitude = "vis"
            OPTIONS.settings.display.label = r"$V$ (a.u.)"
        elif self.vis2_radio.isChecked():
            OPTIONS.settings.display.amplitude = "vis2"
            OPTIONS.settings.display.label = r"$V^2$ (a.u.)"
        self.plots.display_model()

    # TODO: Reimplement this
    # def toggle_coplanar(self) -> None:
    #     """Slot for radio buttons toggled."""
    #     if self.coplanar_true_radio.isChecked():
    #         OPTIONS.display.coplanar = True
    #     elif self.coplanar_false_radio.isChecked():
    #         OPTIONS.display.coplanar = False
    #     self.plots.display_model()

    # TODO: Reimplement this
    # def open_file_dialog(self):
    #     """Open a file dialog to select files to open.
    #
    #     Allows for multiple file opening.
    #     """
    #     file_names, _ = QFileDialog.getOpenFileNames(
    #         self, "Open File", "", "All Files (*);;Text Files (*.txt)"
    #     )
    #
    #     for file_name in file_names:
    #         self.add_file_to_list(file_name)
    #
    # def add_file_to_list(self, file_name: Path):
    #     """Add a file to the list widget."""
    #     text = Path(file_name)
    #     item = QListWidgetItem(self.file_widget)
    #     item.setText(text.name)
    #
    #     widget = QWidget()
    #     layout = QHBoxLayout(widget)
    #     close_button = QPushButton("X")
    #     close_button.clicked.connect(lambda: self.remove_file(item))
    #     layout.addStretch(1)
    #     layout.addWidget(close_button)
    #     layout.addStretch()
    #
    #     widget.setLayout(layout)
    #     item.setSizeHint(widget.sizeHint())
    #     self.file_widget.addItem(item)
    #     self.file_widget.setItemWidget(item, widget)
    #     self.file_manager.add_file(file_name)
    #     self.plots.display_model()
    #
    # def remove_file(self, item):
    #     """Remove a file from the list widget."""
    #     row = self.file_widget.row(item)
    #     self.file_manager.remove_file(item.text())
    #     self.file_widget.takeItem(row)
    #     self.plots.display_model()
