import flet as ft
from Utilities.download_book import download_book


class Book:
    def __init__(self, book_data, app, library_location, page):
        self.app = app
        self.page = page
        self.book_id = book_data["ID"]
        self.title = book_data["Title"]
        self.author = book_data["Author"]
        self.publisher = book_data["Publisher"]
        self.year = book_data["Year"]
        self.pages = book_data["Pages"]
        self.filetype = book_data["Extension"]
        self.download_link = book_data["Direct_Download_Link"]
        self.cover = book_data["Cover"]

        # Card content
        self.card = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.ListTile(
                            title=ft.Text(self.title),
                            subtitle=ft.Text(self.author),
                            height=200,
                        ),
                        ft.Row(
                            [
                                ft.IconButton(
                                    icon=ft.icons.DOWNLOAD,
                                    on_click=lambda e: download_book(
                                        self,
                                        library_location,
                                        self.page,
                                    ),
                                ),
                                ft.IconButton(
                                    icon=ft.icons.FAVORITE,
                                    on_click=self.save_to_favorites,
                                ),
                                ft.IconButton(
                                    icon=ft.icons.MORE, on_click=self.view_details
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.END,
                        ),
                    ]
                ),
                width=100,
                height=100,
                padding=10,
            ),
            width=100,
            height=120,
            elevation=5,
        )

    def view_details(self, e):
        self.app.add_to_book_store(self)
        self.app.display_book_details(self)

    def save_to_favorites(self, e):
        favorites = self.app.page.client_storage.get("favorites")
        book_dict = {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "publisher": self.publisher,
            "year": self.year,
            "pages": self.pages,
            "filetype": self.filetype,
            "cover": self.cover,
            "download_link": self.download_link,
        }
        if not book_dict in favorites:
            favorites.append(book_dict)
            self.app.page.client_storage.set("favorites", favorites)
