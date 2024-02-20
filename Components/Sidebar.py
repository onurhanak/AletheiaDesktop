import flet as ft


class Sidebar:
    def __init__(
        self,
            page: object,
            open_settings_callback: object,
            open_search_callback: object,
            open_library_callback: object,
            open_favorites_callback: object,
            open_downloads_callback: object,
    ):
        self.selected_color = page.client_storage.get('color_seed')
        self.sidebar_items = [
            ft.IconButton(
                icon=ft.icons.SEARCH_SHARP,
                
                icon_size=40,
                on_click=open_search_callback,
                selected_icon_color=self.selected_color,
                selected=True,
                tooltip="Search"
            ),
            ft.IconButton(
                icon=ft.icons.LIBRARY_BOOKS,
                on_click=open_library_callback,  # Use the passed callback
                icon_size=40,
                selected_icon_color=self.selected_color,
                tooltip="Library"
            ),
            ft.IconButton(
                icon=ft.icons.FAVORITE,
                
                on_click=open_favorites_callback,  # Use the passed callback
                icon_size=40,
                selected_icon_color=self.selected_color,
                tooltip="Favorites"
            ),
            ft.IconButton(
                icon=ft.icons.DOWNLOADING_SHARP,
                
                icon_size=40,
                on_click=open_downloads_callback,
                selected_icon_color=self.selected_color,
                tooltip="Downloads"
            ),
            ft.IconButton(
                icon=ft.icons.SETTINGS,
                
                icon_size=40,
                on_click=open_settings_callback,  # Use the passed callback
                selected_icon_color=self.selected_color,
                tooltip="Settings"
            ),
        ]

        self.sidebar = ft.Container(
            content=ft.Column(
                controls=self.sidebar_items,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=100,
            ),
            width=80,
            height=page.window_height,
            border_radius=10,
        )
    
    def set_selected_button(self, selected_button):
        for button in self.sidebar_items:
            button.selected = (button == selected_button)