import flet as ft


def load_theme(page, color_scheme_seed=None):
    """
    Utility to change theme.
    """
    if not color_scheme_seed:
        color_scheme_seed = page.client_storage.get("color_seed")

    theme = page.client_storage.get("theme")

    if theme == "Light":
        page.theme = ft.theme.Theme(color_scheme_seed=color_scheme_seed)
        page.theme_mode = "LIGHT"
    elif theme == "Dark":
        page.theme = ft.theme.Theme(color_scheme_seed=color_scheme_seed)
        page.theme_mode = "DARK"

    return
