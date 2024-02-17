import flet as ft
from Components.SearchArea import SearchArea


class MainView:
    def __init__(self, page, results_instance):
        self.results_instance = results_instance
        self.search_area = SearchArea(page, self.results_instance).search_area
        self.search_area_row = ft.Row(controls=[self.search_area], alignment=ft.MainAxisAlignment.CENTER, expand=0, height=50)
        self.results_row = results_instance.results
        self.main_area = ft.Container(
            content=ft.Column(
                controls=[self.search_area_row, self.results_row],
                spacing=10,
                height=page.window_height,
                width=page.window_width,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=1),
            padding=20,
            height=page.window_height,
            width=page.window_width)
