import flet as ft


class Sidebar:
    def __init__(
        self,
        page,
        open_settings_callback,
        open_search_callback,
        open_library_callback,
        open_favorites_callback,
    ):

        self.sidebar_items = [
            ft.IconButton(
                icon=ft.icons.SEARCH_SHARP,
                # icon_color=buttonBackground,
                icon_size=40,
                on_click=open_search_callback,
                selected_icon_color=ft.colors.RED,
                tooltip="Search"
            ),
            ft.IconButton(
                icon=ft.icons.LIBRARY_BOOKS,
                # icon_color=buttonBackground,
                on_click=open_library_callback,  # Use the passed callback
                icon_size=40,
                selected_icon_color=ft.colors.RED,
                tooltip="Library"
            ),
            ft.IconButton(
                icon=ft.icons.FAVORITE,
                # icon_color=buttonBackground,
                on_click=open_favorites_callback,  # Use the passed callback
                icon_size=40,
                selected_icon_color=ft.colors.RED,
                tooltip="Favorites"
            ),
            ft.IconButton(
                icon=ft.icons.SETTINGS,
                # icon_color=buttonBackground,
                icon_size=40,
                on_click=open_settings_callback,  # Use the passed callback
                selected_icon_color=ft.colors.RED,
                tooltip="Settings"
            ),
        ]

        self.sidebar = ft.Container(
            content=ft.Column(
                controls=self.sidebar_items,
                alignment="CENTER",
                horizontal_alignment="CENTER",
                spacing=150,
            ),
            width=80,
            height=page.window_height,
            border_radius=10,
        )
