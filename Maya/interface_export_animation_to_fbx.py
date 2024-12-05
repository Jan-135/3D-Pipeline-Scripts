# Standard library imports
from typing import Optional

# Third-party imports
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox, 
    QPushButton, QHBoxLayout, QMessageBox, QMainWindow
)
from PySide6.QtCore import Qt
from shiboken6 import wrapInstance
import maya.OpenMayaUI as omui

# Local application imports
import export_animation_to_fbx as export


class MyWidget(QWidget):
    """
    A custom QWidget providing a user interface for selecting a scene and character
    and exporting the animation.
    """

    def __init__(self) -> None:
        """Initializes the widget with its layout and components."""
        super().__init__()

        self.setWindowTitle("Exporting Animation")
        self.setMinimumWidth(500)

        main_layout = QVBoxLayout()

        self.label = QLabel("Select an option:")
        main_layout.addWidget(self.label)

        self.scene_dropdown = QComboBox()
        self.scene_dropdown.addItem("Please select a scene")  # Placeholder option
        for i in range(1, 21):
            self.scene_dropdown.addItem(f"Szene{i:03}")
        main_layout.addWidget(self.scene_dropdown)

        self.character_dropdown = QComboBox()
        self.character_dropdown.addItem("Please select a character")  # Placeholder option
        self.character_dropdown.addItems(["Maurice", "Golem_Mother", "Bird", "Test"])
        main_layout.addWidget(self.character_dropdown)

        h_layout = QHBoxLayout()

        export_button = QPushButton("Export")
        export_button.clicked.connect(self.clicked_export_button)
        h_layout.addWidget(export_button)

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.clicked_cancel_button)
        h_layout.addWidget(cancel_button)

        main_layout.addLayout(h_layout)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        self.setLayout(main_layout)

    def clicked_export_button(self) -> None:
        """
        Handles the export button click event.
        Validates selections and initiates the export process.
        """
        selected_scene = self.scene_dropdown.currentText()
        selected_character = self.character_dropdown.currentText()

        if selected_scene == "Please select a scene" or selected_character == "Please select a character":
            QMessageBox.warning(self, "Invalid Selection", "Please select both a scene and a character before exporting.")
            return

        print(f"Exported: Scene = {selected_scene}, Character = {selected_character}")

        check = export.execute(selected_scene, selected_character)
        if check:
            QMessageBox.information(
                self,
                "Export Successful",
                "The export was successful!",
                QMessageBox.Ok
            )
            self.close()  # Close the current widget
            self.parentWidget().close()  # Close the parent window (QMainWindow)
        else:
            QMessageBox.warning(
                self,
                "Export Failed",
                "Something went wrong during the export.",
                QMessageBox.Ok
            )

    def clicked_cancel_button(self) -> None:
        """
        Handles the cancel button click event.
        Prompts the user for confirmation before closing the window.
        """
        reply = QMessageBox.question(
            self,
            "Confirm Exit",
            "Are you sure you want to cancel?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.parentWidget().close()


def maya_main_window() -> QWidget:
    """
    Retrieves the Maya main window as a Qt object, allowing PySide6 integration.

    Returns:
        QWidget: The main window of Maya wrapped as a Qt widget.
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QWidget)


class MyWindow(QMainWindow):
    """
    The main application window for selecting a scene and character.
    """

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        Initializes the main window for the application.

        Args:
            parent (Optional[QWidget]): The parent widget, usually the Maya main window.
        """
        super(MyWindow, self).__init__(parent)

        self.setWindowTitle("Select Scene and Character")
        self.resize(500, 100)

        widget = MyWidget()
        self.setCentralWidget(widget)


def execute() -> None:
    """
    Executes the main workflow: creating and displaying the window,
    and running the export process upon user interaction.
    """
    print("Application started")
    parent = maya_main_window()

    window = MyWindow(parent=parent)
    window.show()
