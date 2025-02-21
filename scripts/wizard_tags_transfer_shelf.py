import maya.cmds as cmds
import maya.utils
import os

def add_shelf_button():
    shelf = "Custom"
    
    # Get the path of the current script folder (Wizard_Tags_Transfer directory)
    script_dir = os.path.dirname(__file__)
    
    # Define the relative path to the icon
    icon_path = os.path.join(script_dir, "..", "icons", "wizard_tags_transfer_icon.svg")
    
    # Ensure the shelf "Custom" exists, create it if it doesn't
    if not cmds.shelfLayout(shelf, exists=True):
        shelf = cmds.shelfLayout(shelf, parent="ShelfLayout")
    
    # Add the shelf button to the "Custom" shelf
    cmds.shelfButton(
        label="Wizard_Tags_Transfer",
        command="import Wizard_Tags_Transfer.wizard_tags_transfer_launcher; Wizard_Tags_Transfer.wizard_tags_transfer_launcher.launch()",
        image=icon_path,
        annotation="Launch Wizard_Tags_Transfer",
        parent=shelf  # Explicitly set the parent to the "Custom" shelf
    )

# Use executeDeferred to ensure the button is added after Maya initializes
def add_shelf_button_deferred():
    maya.utils.executeDeferred(add_shelf_button)
