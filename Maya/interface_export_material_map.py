from PySide6.QtWidgets import QWidget, QPushButton, QMainWindow
from shiboken6 import wrapInstance
import maya.OpenMayaUI as omui
from PySide6.QtWidgets import QLineEdit, QHBoxLayout, QVBoxLayout, QLabel, QFileDialog
from PySide6.QtCore import Qt, QTimer

class Widget(QWidget):
    def __init__(self):
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

        # Set alignment to the top of the window
        v_layout.setAlignment(Qt.AlignTop)

        self.setLayout(v_layout)

    def cancel_button_clicked(self):
        # Close the parent window (MyWindow) by accessing the parent
        parent = self.parentWidget()  # Get the parent widget
        if parent:
            parent.close()  # Close the parent window


    def done_button_clicked(self):
        
        parent = self.parentWidget()
        if self.destination_label.text() == "Nothing selected":
            self.highlight_button(self.open_explorer_button)


            print("No destination selected.")
        else:
            print(f"Destination saved at: {self.destination_label.text()}")
            parent.close()

    def button_clicked(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "default.json", "JSON Files (*.json)")

        if file_path:
            self.destination_label.setText(file_path)
            self.destination_label.setStyleSheet("")
        else:
            self.destination_label.setText("Nothing selected")
            self.destination_label.setStyleSheet("font-style: italic; color: gray;")
            
    def reset_button(self, button):
        """Reset the button's appearance after highlighting."""
        button.setStyleSheet("")  # Reset the style to default
        
    def highlight_button(self, button):
        """Temporarily change the button's background color to highlight it."""
        # Change the button's background color to grab attention
        button.setStyleSheet("background-color: #a0bdb8;")

        # Set a timer to reset the button's style after 500 ms
        QTimer.singleShot(500, lambda: self.reset_button(button))


def maya_main_window():
    """Get the Maya main window as a Qt object."""
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QWidget)

class MyWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)

        self.setWindowTitle("Save JSON file")
        self.resize(500, 100)

        widget = Widget()
        self.setCentralWidget(widget)

# Get Maya's main window as the parent
parent = maya_main_window()

# Create and show the window
window = MyWindow(parent=parent)
window.show()
