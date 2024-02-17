import flet as ft
from Components.Book import Book


class ResultsArea:
    def __init__(self, page, app):
        self.results = ft.GridView(
            expand=1,
            runs_count=5,
            max_extent=300,
            child_aspect_ratio=1,
            spacing=5,
            run_spacing=5,
        )
        self.app = app
        self.page = page
        self.library_location = page.client_storage.get("library")

    def clear(self):
        self.results.controls.clear()

    def populate_results(self, items, page, library_location):
        self.clear()
        for item in items:
            book = Book(item, self.app, library_location, self.page)
            self.results.controls.append(book.card)
        page.update()
