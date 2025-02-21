import Wizard_Tags_Transfer.scripts.wizard_tags_transfer_ui as ui
import Wizard_Tags_Transfer.scripts.wizard_tags_transfer_shelf as wizard_tags_transfer_shelf

def launch():
    ui.run()  # Run the UI

def shelf():
    wizard_tags_transfer_shelf.add_shelf_button_deferred()  # Create the shelf button
