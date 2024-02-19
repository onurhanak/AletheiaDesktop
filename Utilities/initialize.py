import os
import flet as ft
from os.path import expanduser


def ask_for_library_location(page):
    def on_folder_selected(e: ft.FilePickerResultEvent):
        if e.path:
            library_location = e.path
            library_location = f"{library_location}/AletheiaLibrary"
            os.makedirs(f"{library_location}", exist_ok=True)
            page.client_storage.set("library", library_location)
            dlg_modal.open = False
            page.update()

    pick_files_dialog = ft.FilePicker(on_result=on_folder_selected)

    def open_file_picker(e):
        page.add(pick_files_dialog)

        pick_files_dialog.get_directory_path()

    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Initialization"),
        content=ft.Text("Please select a folder for your Aletheia library."),
        actions=[
            ft.TextButton("Select Folder", on_click=open_file_picker),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.dialog = dlg_modal
    dlg_modal.open = True
    page.update()
    return


def initialization(page):
    """
    Triggered when the user runs the application
    for the first time. Set dark theme, create library, create a dummy file.
    """

    user_home_dir = expanduser("~")

    if not os.path.exists(f"{user_home_dir}/.aletheia"):
        page.client_storage.set("dark_theme_selected", True)
        page.client_storage.set("light_theme_selected", False)
        page.client_storage.set("downloaded_books", [])
        page.client_storage.set("favorites", [])
        page.theme = ft.theme.Theme(color_scheme_seed="gray")
        page.theme_mode = "DARK"

        ask_for_library_location(page)

        with open(f"{user_home_dir}/.aletheia", "w") as f:
            pass

    return
