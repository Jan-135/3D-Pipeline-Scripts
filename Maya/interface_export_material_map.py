# Standard library imports
from typing import Optional

# Third-party imports
from PySide6.QtWidgets import QWidget, QPushButton, QMainWindow, QLineEdit, QHBoxLayout, QVBoxLayout, QLabel, QFileDialog
from PySide6.QtCore import Qt, QTimer
from shiboken6 import wrapInstance
import maya.OpenMayaUI as omui

# Local application imports
import export_material_map as export


class Widget(QWidget):
    def __init__(self) -> None:
        """
        Initializes the widget with UI components such as buttons, labels, and layouts.
        """
        super().__init__()

        self.setWindowTitle("Title")
        self.setMinimumWidth(500)

        info_label = QLabel("Select a destination:")
        self.destination_label = QLabel("Nothing selected")
        self.destination_label.setStyleSheet("font-style: italic; color: gray;")

        self.open_explorer_button = QPushButton("Open Explorer")
        self.open_explorer_button.clicked.connect(self.button_clicked)

        done_button = QPushButton("Done")
        done_button.clicked.connect(self.done_button_clicked)

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.cancel_button_clicked)
        cancel_button.setDefault(True)

        h_layout = QHBoxLayout()
        h_layout.addWidget(done_button)
        h_layout.addWidget(cancel_button)

        v_layout = QVBoxLayout()
        v_layout.addWidget(info_label)
        v_layout.addWidget(self.destination_label)
        v_layout.addWidget(self.open_explorer_button)
        v_layout.addLayout(h_layout)

        v_layout.setAlignment(Qt.AlignTop)

        self.setLayout(v_layout)
        
    def button_clicked(self) -> None:
        """
        Opens a file dialog to select a save location for the JSON file.
        """
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "JSON Files (*.json)")

        if file_path:
            self.destination_label.setText(file_path)
            self.destination_label.setStyleSheet("") 
        else:
            self.destination_label.setText("Nothing selected")
            self.destination_label.setStyleSheet("font-style: italic; color: gray;")
            
    def cancel_button_clicked(self) -> None:
        """
        Closes the parent window when the cancel button is clicked.
        """
        parent = self.parentWidget()
        if parent:
            parent.close()

    def done_button_clicked(self) -> None:
        """
        Executes the action of saving the data to the selected path when the done button is clicked.
        """
        parent = self.parentWidget()
        output_path = self.destination_label.text()

        if self.destination_label.text() == "Nothing selected":
            self.highlight_button(self.open_explorer_button)
            print("No destination selected.")
        else:
            print(f"Destination saved at: {self.destination_label.text()}")
            parent.close()
            export.execute(output_path)

    def reset_button(self, button: QPushButton) -> None:
        """
        Resets the button's appearance after highlighting.
        
        Args:
            button (QPushButton): The button whose appearance needs to be reset.
        """
        button.setStyleSheet("")
        
    def highlight_button(self, button: QPushButton) -> None:
        """
        Temporarily highlights the button by changing its background color.
        
        Args:
            button (QPushButton): The button to highlight.
        """
        button.setStyleSheet("background-color: #a0bdb8;")

        QTimer.singleShot(500, lambda: self.reset_button(button))


def maya_main_window() -> QWidget:
    """
    Retrieves the Maya main window as a Qt object, allowing PySide6 integration.

    Returns:
        QWidget: The main window of Maya wrapped as a Qt widget.
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QWidget)


class MyWindow(QMainWindow):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        Initializes the main window for the application.

        Args:
            parent (Optional[QWidget]): The parent widget, usually the Maya main window.
        """
        super(MyWindow, self).__init__(parent)

        self.setWindowTitle("Save JSON file")
        self.resize(500, 100)

        widget = Widget()
        self.setCentralWidget(widget)


def execute() -> None:
    """
    Executes the main workflow: creating and displaying the window, 
    and running the export process upon user interaction.
    """
    print("Geschafft")
    parent = maya_main_window()

    window = MyWindow(parent=parent)
    window.show()
