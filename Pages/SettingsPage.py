import flet as ft
from Utilities.theme_utils import load_theme
from flet_contrib.color_picker import ColorPicker

class Settings:
    def __init__(self, page: ft.Page, sidebar):
        self.page = page
        self.sidebar = sidebar

        self.color_picker = ColorPicker(color="#c8df6f", width=300)

        self.color_icon = ft.IconButton(icon=ft.icons.BRUSH, on_click=self.open_color_picker)

        self.d = ft.AlertDialog(
            content=self.color_picker,
            actions=[
                ft.TextButton("OK", on_click=self.change_color),
                ft.TextButton("Cancel", on_click=self.close_dialog),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=self.change_color,
            open=False  
        )

        self.file_picker = ft.FilePicker()

        self.pick_file_dialog = ft.FilePicker(on_result=self.pick_file_result)
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
            on_change=self.on_theme_change,
        )

        title = ft.Text("Settings", size=32, weight=ft.FontWeight.BOLD, text_align="center")

        self.color_seed_element = ft.Row(
            controls=[
                ft.Text("Theme color seed: ", size=20),
                self.color_icon,
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
        self.settings_layout = ft.Column(
            controls=[
                title,
                self.color_seed_element,  
                ft.Row(
                    controls=[
                        self.download_location_text,
                        self.pick_folder_button,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                self.theme,
                self.d,  
            ],
            expand=1,
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def open_color_picker(self, e):
        self.d.open = True
        self.page.update()

    def change_color(self, e):
        self.color_icon.icon_color = self.color_picker.color
        self.page.client_storage.set('color_seed', self.color_picker.color)
        self.d.open = False
        load_theme(self.page, self.color_picker.color)
        self.page.update()

    def close_dialog(self, e):
        self.d.open = False
        self.page.update()



    def pick_file_result(self, e: ft.FilePickerResultEvent):
        if e.files:
            folder_path = e.files[0].path.rsplit("/", 1)[0]
            self.download_location_text.value = folder_path
        else:
            self.download_location_text.value = "No folder selected"
        self.download_location_text.update()
        self.page.client_storage.set("library", folder_path)

    def on_theme_change(self, e):
        self.page.client_storage.set("theme", e.control.value)
        load_theme(self.page)  # Pass the page instance
        self.page.update()

    def render(self):
        return self.settings_layout
