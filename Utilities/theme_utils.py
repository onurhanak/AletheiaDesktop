import flet as ft


def load_theme(page):
    """
    Utility to change theme.
    """
    theme = page.client_storage.get("theme")

    if theme == "Light":
        page.theme = ft.theme.Theme(color_scheme_seed="purple")
        page.theme_mode = "LIGHT"
    elif theme == "Dark":
        page.theme = ft.theme.Theme(color_scheme_seed="purple")
        page.theme_mode = "DARK"

    return None