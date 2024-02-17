import flet as ft
from flet import Page, RouteChangeEvent, View, ViewPopEvent

from Components.MainView import MainView
from Components.ResultsArea import ResultsArea
from Components.Sidebar import Sidebar
from Pages.LibraryPage import Library
from Pages.FavoritesPage import Favorites
from Pages.SettingsPage import Settings
from Utilities.download_book import download_book
from Utilities.theme_utils import load_theme
from Utilities.initialize import initialization


class AletheiaApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.book_store = {}
        self.sidebar = Sidebar(
            self.page, self.open_settings, self.open_search_page, self.open_library_page, self.open_favorites_page
        )

        self.results_instance = ResultsArea(self.page, self)
        self.main_view = MainView(self.page, self.results_instance)
        self.settings = Settings(self.page, self.sidebar)
        self.library = Library(self.page)
        self.favorites = Favorites(self.page)
        self.content_layout = ft.Column(
            controls=[self.main_view.main_area], expand=1, spacing=0
        )

        self.setup_initial_view()
        self.setup_page_callbacks()
        initialization(page)
        load_theme(page)


    def setup_initial_view(self):
        self.main_layout = self.create_main_layout()
        self.add_results_area()

        initial_view = View(route="/", controls=[self.main_layout])
        self.page.views.append(initial_view)
        self.page.update()

    def create_main_layout(self):
        return ft.Row(
            controls=[
                self.sidebar.sidebar,
                ft.Column(controls=[self.main_view.search_area], expand=1),
            ],
            expand=1,
        )

    def add_to_book_store(self, book):
        self.book_store[book.book_id] = book

    def add_results_area(self):
        results_column = self.main_layout.controls[1]
        results_column.controls.append(self.main_view.results_row)
        self.page.update()

    def setup_page_callbacks(self):
        self.page.on_route_change = self.route_change
        self.page.on_view_pop = self.view_pop

    def open_search_page(self, event=None):
        self.page.views.clear()

        main_layout = ft.Row(
            controls=[
                self.sidebar.sidebar,
                ft.Column(
                    controls=[
                        self.main_view.search_area,
                        self.main_view.results_row  # Include the results row
                    ],
                    expand=1,
                ),
            ],
            expand=1,
        )

        self.page.views.append(
            View(
                route="/",
                controls=[main_layout],
            )
        )
        self.page.update()

    def open_library_page(self, event=None):
        self.library = Library(self.page)
        self.change_page_layout("/library", self.library.library_view)

    def open_favorites_page(self, event=None):
        self.favorites = Favorites(self.page)  # create a new instance so it will update with the faved books.
        self.change_page_layout("/favorites", self.favorites.library_view)


    def open_settings(self, event=None):
        settings_view = self.settings.render()
        self.change_page_layout("/settings", settings_view)

    def change_page_layout(self, route, new_control=None):
        self.page.views.clear()
        layout_controls = [self.sidebar.sidebar]
        if new_control:
            layout_controls.append(new_control)
        main_layout = ft.Row(controls=layout_controls, expand=1)
        self.page.views.append(View(route=route, controls=[main_layout]))
        self.page.update()

    def route_change(self, e: RouteChangeEvent):
        if e.route == "/":
            self.open_search_page()
        elif e.route.startswith("/book/"):
            book_id = e.route.split("/")[2]
            book = self.book_store.get(book_id)
            if book:
                self.display_book_details(book)
        elif e.route.startswith("/settings"):
            self.open_settings()
        elif e.route.startswith("/library"):
            self.open_library_page()
        elif e.route.startswith("/favorites"):
            self.open_favorites_page()

    def display_book_details(self, book):
        dialog = self.create_book_details_dialog(book)
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()


    def create_book_details_dialog(self, book):
        book_cover = ft.Image(
            src=book.cover, width=400, height=400, fit=ft.ImageFit.CONTAIN, border_radius=5
        )
        library_location = self.page.client_storage.get("library")

        book_details_controls = [
            ft.Text(value=book.title, size=24, weight=ft.FontWeight.BOLD),
            ft.Text(value=f"Author: {book.author}", size=16),
            ft.Text(value=f"Publisher: {book.publisher}", size=16),
            ft.Text(value=f"Year: {book.year}", size=16),
            ft.Text(value=f"Pages: {book.pages}", size=16),
            ft.Text(value=f"File Type: {book.filetype}", size=16),
            ft.IconButton(
                icon=ft.icons.DOWNLOAD,
                on_click=lambda e: download_book(
                    book, library_location, self.page
                ),
            ),
        ]

        book_details_column = ft.Column(
            controls=book_details_controls, expand=1, spacing=10, alignment=ft.MainAxisAlignment.CENTER,
        )

        dialog_content = ft.Row(
            controls=[book_cover, book_details_column],
            expand=1,
            alignment=ft.MainAxisAlignment.CENTER,
            width=800,
            height=600
        )

        # Create dialog
        book_dialog = ft.AlertDialog(
            content=dialog_content,
            modal=False,
            content_padding=20,
            inset_padding=0,
            
        )
        return book_dialog
    
    def close_dialog(self):
        self.page.dialog.open = False
        self.page.update()

    def go_back_to_results(self, e):
        self.open_search_page()

    def view_pop(self, e: ViewPopEvent):
        self.page.views.pop()
        top_view = self.page.views[-1]
        self.page.go(top_view.route)


if __name__ == "__main__":

    def main(page: Page):
        page.title = "Aletheia"
        app = AletheiaApp(page)
        page.update()

    ft.app(target=main)
