from PySide2 import QtWidgets
from PySide2.QtWidgets import QMessageBox  # Import QMessageBox from PySide2
import maya.cmds as cmds
import maya.OpenMaya as om

# Global dictionary to store object data
object_data = {}  # Dictionary: { "object": "attribute_value" }
attribute_name = "wizardTags"  # Attribute to check

def add_object(referent_list_widget=None):
    """Add an object to the dictionary if it has wizardTags"""
    selected_objects = cmds.ls(selection=True)
    
    if not selected_objects:
        om.MGlobal.displayError("No object selected!")
        return

    for obj in selected_objects:
        if cmds.attributeQuery(attribute_name, node=obj, exists=True):
            if obj not in object_data:
                object_data[obj] = cmds.getAttr(f"{obj}.{attribute_name}")
                print(f" Added {obj} with value {object_data[obj]}")
            else:
                om.MGlobal.displayWarning(f" {obj} already exists in the dictionary.")
        else:
            om.MGlobal.displayError(f"{obj} doesn't have 'wizardTags' attribute.")

    print("Current object_data:", object_data)

    # After adding objects, update the list widget in the UI (optional)
    if referent_list_widget:
        referent_list_widget.clear()  # Clear the list first
        for obj_name in object_data:
            referent_list_widget.addItem(obj_name)  # Add the object name to the list

def remove_object(referent_list_widget):
    """Remove the selected object from the dictionary and list"""
    selected_item = referent_list_widget.currentItem()

    if selected_item:
        obj_name = selected_item.text()

        # Remove from dictionary
        if obj_name in object_data:
            del object_data[obj_name]
            om.MGlobal.displayInfo(f"Removed {obj_name} from the dictionary!")

        # Remove from QListWidget
        row = referent_list_widget.row(selected_item)
        referent_list_widget.takeItem(row)
    else:
        om.MGlobal.displayError("No object selected to remove.")

def display_attribute_value(current_object):
    """Display the stored Wizard Tags attribute value"""
    if current_object in object_data:
        return str(object_data[current_object])
    
    return ""

def transfer_wizard_tags(get_tags):
    """Transfers wizard tags while handling overwrite prompts properly."""
    selected_objects = cmds.ls(selection=True, long=True)
    if not selected_objects:
        om.MGlobal.displayError("No objects selected!")
        return

    transforms_to_select = []

    # Find all valid transforms
    for obj in selected_objects:
        if cmds.objectType(obj, isType="transform"):
            descendants = cmds.listRelatives(obj, allDescendents=True, fullPath=True) or []
            non_group_transforms = [
                node for node in cmds.ls(descendants, type="transform")
                if not cmds.listRelatives(node, children=True, type="transform")
            ]

            if not cmds.listRelatives(obj, children=True, type="transform"):
                transforms_to_select.append(obj)
            
            transforms_to_select.extend(non_group_transforms)

    transforms_to_select = list(set(transforms_to_select))
    overwrite_all = None  # Track user's overwrite choice

    # Process each transform
    for transform in transforms_to_select:
        if not cmds.attributeQuery(attribute_name, node=transform, exists=True):
            cmds.addAttr(transform, longName=attribute_name, dataType="string")

        current_tags = cmds.getAttr(f"{transform}.{attribute_name}") or ""

        # Ask user only once
        if current_tags and overwrite_all is None:
            msgBox = QMessageBox()
            msgBox.setText("Wizard Tags found")
            msgBox.setInformativeText("Some objects already have Wizard Tags. Overwrite?")
            msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msgBox.setDefaultButton(QMessageBox.No)
            ret = msgBox.exec()

            overwrite_all = (ret == QMessageBox.Yes)

        # Skip updating if the user selected "No"
        if current_tags and not overwrite_all:
            om.MGlobal.displayWarning(f"Skipping {transform}, existing tags not overwritten.")
            return

        # Now safely update the attribute
        cmds.setAttr(f"{transform}.{attribute_name}", get_tags, type="string")

    om.MGlobal.displayInfo("Wizard tags successfully added to selected objects!")