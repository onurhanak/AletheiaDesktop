import flet as ft
import subprocess, os, platform

class Library:
    def __init__(self, page: ft.Page):
        self.page = page
        self.downloaded_books = page.client_storage.get("downloaded_books") or []

        self.library_view = self.create_library_view()
        self.display_books()

    def create_library_view(self):
        # Create a layout for the library (e.g., a grid or a list)
        return ft.GridView(
            expand=1,
            runs_count=5,
            max_extent=300,
            child_aspect_ratio=1,
            spacing=5,
            run_spacing=5,
            padding=20
        )

    def display_books(self):
        self.library_view.controls.clear()

        for book in self.downloaded_books:
            card = self.create_book_card(book)
            self.library_view.controls.append(card)

        # Update the page
        self.page.update()

    def create_book_card(self, book):
        # Create a card for a single book
        card_width = 300
        card_height = 300

        open_button = ft.IconButton(
            icon=ft.icons.OPEN_IN_BROWSER,
            on_click=lambda _: self.open_book(book),
            icon_color=ft.colors.WHITE
        )

        delete_button = ft.IconButton(
            icon=ft.icons.DELETE,
            on_click=lambda _: self.delete_book(book),
            icon_color=ft.colors.WHITE

        )

        return ft.Card(
            content=ft.Stack(
                [
                    ft.ShaderMask(
                        ft.Image(
                            src=book["cover"],
                            width=card_width,
                            height=card_height,
                            fit=ft.ImageFit.FILL,
                            border_radius=4,
                        ),
                        blend_mode=ft.BlendMode.MULTIPLY,
                        shader=ft.RadialGradient(
                            center=ft.alignment.center,
                            radius=2.0,
                            colors=[ft.colors.GREY_600],
                            tile_mode=ft.GradientTileMode.CLAMP,
                        ),
                    ),
                    ft.Column(
                    controls=[
                        ft.Text(
                            book["title"],
                            color="white",
                            size=20,
                            weight="bold",
                            text_align="center",
                        ),
                        ft.Text(
                            book["author"],
                            color="white",
                            size=20,
                            weight="bold",
                            text_align="center",
                        ),
                        ft.Row(
                                controls=[open_button, delete_button],
                                alignment=ft.MainAxisAlignment.CENTER,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    width=card_width,
                    height=card_height,
                ),
                ],
                width=card_width,
                height=card_height,
            ),
            width=card_width,
            height=card_height,
            elevation=5,
            
        )

    def open_book(self, book):
        filepath = book['file_path']
        if platform.system() == 'Darwin':       # macOS
            subprocess.call(('open', filepath))
        elif platform.system() == 'Windows':    # Windows
            os.startfile(filepath)
        else:                                   # linux variants
            subprocess.call(('xdg-open', filepath))

    def delete_book(self, book):
        os.remove(book['file_path'])
        self.downloaded_books.remove(book)
        self.page.client_storage.set("downloaded_books", self.downloaded_books)
        self.display_books()
