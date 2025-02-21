import maya.cmds as cmds
from PySide2.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget, QFrame, QSpacerItem, QSizePolicy, QWidget
)
from PySide2.QtGui import QIcon
from PySide2.QtCore import Qt
import shiboken2
import maya.OpenMayaUI as omui
import maya.OpenMaya as om
import os
import Wizard_Tags_Transfer.scripts.wizard_tags_transfer_utils as utils  # Import your logic module

def maya_main_window():
    """Get Maya's main window as a QWidget."""
    main_window_ptr = omui.MQtUtil.mainWindow()
    return shiboken2.wrapInstance(int(main_window_ptr), QDialog)


def get_abspath(relative_path):
    """Returns the absolute path of a file inside the script's directory."""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(base_dir, relative_path).replace("\\", "/")


class WizardTagsTransfer(QDialog):
    def __init__(self, parent=maya_main_window()):
        super(WizardTagsTransfer, self).__init__(parent)
        self.setWindowFlags(Qt.Window | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        self.setModal(False)
        self.setWindowTitle("Wizard Tags Transfer")
        self.resize(400, 600)

        self.current_name = None  # Initialize current_name
        self.init_ui()
        self.load_stylesheet()
        self.setWindowIcon(QIcon(get_abspath("icons/wizard_tags_transfer_icon.svg")))
        self.show()

    def load_stylesheet(self):
        """Loads the external stylesheet."""
        stylesheet_path = get_abspath("icons/stylesheet.css")
        if os.path.exists(stylesheet_path):
            with open(stylesheet_path, "r") as f:
                stylesheet = f.read()
                self.setStyleSheet(stylesheet)
        else:
            print(f"Warning: Stylesheet not found at {stylesheet_path}")

    def init_ui(self):
        """Initialize UI elements."""
        main_layout = QVBoxLayout(self)

        # Header Layout
        header_layout = QHBoxLayout()
        self.referent_label = QLabel("Select referent objects:")
        header_layout.addWidget(self.referent_label)

        header_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.add_referent_button = QPushButton(" Add ")
        self.add_referent_button.clicked.connect(self.add_object)
        self.remove_referent_button = QPushButton("Remove")
        self.remove_referent_button.clicked.connect(self.remove_object)
        header_layout.addWidget(self.add_referent_button)
        header_layout.addWidget(self.remove_referent_button)

        main_layout.addLayout(header_layout)

        # Referent List Widget
        self.referent_list_widget = QListWidget()
        self.referent_list_widget.setObjectName("referent_list_widget")  # Set objectName
        self.referent_list_widget.currentItemChanged.connect(self.update_selected_object_label)
        main_layout.addWidget(self.referent_list_widget)

        # Horizontal Line
        self.h_line_1 = QFrame()
        self.h_line_1.setFrameShape(QFrame.HLine)
        self.h_line_1.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(self.h_line_1)

        # Wizard Object Display
        wizard_layout = QVBoxLayout()
        self.wizard_object_label = QLabel("Wizard tags on selected object:")
        self.wizard_tags_label = QLabel(" -- Select a referent object -- ")  # Placeholder text
        self.wizard_tags_label.setObjectName("wizard_tags_label")  # Set objectName
        wizard_layout.addWidget(self.wizard_object_label)
        wizard_layout.addWidget(self.wizard_tags_label)
        main_layout.addLayout(wizard_layout)

        # Horizontal Line
        self.h_line_2 = QFrame()
        self.h_line_2.setFrameShape(QFrame.HLine)
        self.h_line_2.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(self.h_line_2)

        # Transfer Button
        self.transfer_button = QPushButton("Transfer")
        self.transfer_button.clicked.connect(self.transfer_tags)
        main_layout.addWidget(self.transfer_button)

        # Set main layout
        self.setLayout(main_layout)

        # Initial population of the list
        self.populate_list()

    def populate_list(self):
        """Populate the list widget with object names from object_data."""
        self.referent_list_widget.clear()  # Clear existing items

        for obj_name in utils.object_data:
            self.referent_list_widget.addItem(obj_name)  # Add item to the widget

    def add_object(self):
        """Add selected objects to the dictionary and update the UI."""
        utils.add_object(self.referent_list_widget)  # Add objects to the dictionary
        self.populate_list()  # Update the UI list after adding

    def remove_object(self):
        """Remove selected object from the dictionary and update the UI."""
        utils.remove_object(self.referent_list_widget)  # Remove objects from the dictionary
        self.populate_list()  # Update the UI list after removing

    def update_selected_object_label(self, current_item):
        """Update the label to show the wizardTags value of the selected object"""
        if current_item:
            # Get the name of the selected object
            self.current_name = current_item.text()
            wizard_tag_value = utils.display_attribute_value(self.current_name)
            self.wizard_tags_label.setText(wizard_tag_value)
        else:
            self.current_name = None  # No selection
            self.wizard_tags_label.setText(" -- Select a referent object -- ")  # Reset UI
    
    def transfer_tags(self):
        """Transfers wizard tags from the selected object."""
        if self.current_name:
            get_tags =utils.display_attribute_value(self.current_name)
            utils.transfer_wizard_tags(get_tags)
        else:
            om.MGlobal.displayError("No wizard tags selected to transfer!")

def run():
    """Launch the UI."""
    global wizard_tags_transfer_window
    try:
        wizard_tags_transfer_window.close()
        wizard_tags_transfer_window.deleteLater()
    except:
        pass
    wizard_tags_transfer_window = WizardTagsTransfer()
