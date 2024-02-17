import flet as ft
from Utilities.theme_utils import load_theme

class Settings:
    def __init__(self, page: ft.Page, sidebar):
        self.page = page
        self.sidebar = sidebar
        def folder_picker_result(e: ft.FilePickerResultEvent):
            print("Selected file or directory:", e.path)

        self.file_picker = ft.FilePicker(on_result=folder_picker_result)

        def pick_file_result(e: ft.FilePickerResultEvent):
            if e.files:
                folder_path = e.files[0].path.rsplit("/", 1)[0]
                self.download_location_text.value = folder_path
            else:
                self.download_location_text.value = "No folder selected"
            self.download_location_text.update()
            self.page.client_storage.set("library", folder_path)

        def on_theme_change(e):
            self.page.client_storage.set("theme", e.control.value)
            load_theme(page)  # Pass the sidebar instance
            self.page.update()

        self.pick_file_dialog = ft.FilePicker(on_result=pick_file_result)
        self.page.overlay.append(self.pick_file_dialog)

        self.download_location_text = ft.TextField(label=self.page.client_storage.get('library'), width=200)
        self.pick_folder_button = ft.IconButton(
            icon=ft.icons.FOLDER_OPEN,
            on_click=lambda _: self.pick_file_dialog.pick_files()
        )

        self.theme = ft.Dropdown(
            label=self.page.client_storage.get("theme"),
            options=[
                ft.dropdown.Option(text="Light"),
                ft.dropdown.Option(text="Dark"),
            ],
            width=250,
            on_change=on_theme_change,
        )

        self.settings_layout = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        self.download_location_text,
                        self.pick_folder_button,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                self.theme,
            ],
            expand=1,
            spacing=12,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def render(self):
        return self.settings_layout
