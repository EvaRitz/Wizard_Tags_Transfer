# Wizard tags transfer

Wizard Tags Transfer is a tool designed for Maya. It's purpose is to transfer wizardTags attributes from one mesh to another. It's a solution to reintegrate meshes into the Wizard Software Pipeline.

## Maya Version

Wizard Tags Transfer was designed on Maya 2024. If your version is 2025 or more, this plugin won't be supported.

## Installation 

* Download this repository into your maya scripts folder under your maya home folder, usually at "C:\Users\YourUserName\Documents\maya\scripts" 

* Open Maya and launch the Script Editor

* Paste the following code

```python
import Wizard_Tags_Transfer.wizard_tags_transfer_launcher
Wizard_Tags_Transfer.wizard_tags_transfer_launcher.launch()
Wizard_Tags_Transfer.wizard_tags_transfer_launcher.shelf()
```

It will create a Button on the Custom Shelf of Maya with this icon ![alt text](icons/wizard_tags_transfer_icon.svg)

## How to use

* Select the meshes whose Wizard tags you wish to reapply on your new meshes

* If you want to remove one of the meshes from the list you can select it and click "remove" 

* To transfer the Wizard attributes, select your mesh in the outliner, and your mesh in the List visible in the widget and select "transfer"
![alt text](tutorial_Wizard_Tags_Transfer.gif)

Additionally, you can't add meshes that don't have Wizard Tags into the list widget, you can select a folder in your outliner or multiples meshes to transfer the data all at once.
As a security, if a mesh already has wizardTags attributes, it will as for permission to override.

## License

Wizard_Tags_Transfer is available under the MIT License. You can use it for commercial or non-commercial projects. Be sure to credit me in the project and documentation.

## Project status

Update from Pyside2 to Pyside6 for Maya versions 2025 and after.

Update the flickering in the wizard tags box (doesn't affect the functionality)
