import flet as ft


class BookPage:
    def __init__(self, page, book_data):
        self.book_id = book_data["ID"]
        self.title = book_data["Title"]
        self.author = book_data["Author"]
        self.publisher = book_data["Publisher"]
        self.year = book_data["Year"]
        self.pages = book_data["Pages"]
        self.filetype = book_data["Extension"]

        info = ft.Row(
            controls=[
                ft.Text(value=self.book_id),
                ft.Text(value=self.author),
                ft.Text(value=self.publisher),
                ft.Text(value=self.year),
                ft.Text(value=self.pages),
                ft.Text(value=self.filetype),
            ]
        )

        page.add(info)
