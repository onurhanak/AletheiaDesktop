import os
from pathlib import Path
import flet as ft
from os.path import expanduser

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

        library_location = f'{user_home_dir}/AletheiaLibrary'

        with open(f"{user_home_dir}/.aletheia", 'w') as f:
            pass

        os.makedirs(library_location, exist_ok=True)
        page.client_storage.set('library', library_location)
        page.client_storage.set('downloaded_books', [])
    return
