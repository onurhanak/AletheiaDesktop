import flet as ft
from libgen_api_enhanced import LibgenSearch


class SearchArea:
    def __init__(self, page, results_instance):
        self.query_type = ft.Dropdown(
                width=100,
                label="Query",
                value="Title",
                options=[
                    ft.dropdown.Option("Title"),
                    ft.dropdown.Option("Author"),
                ],
            )
        self.user_query = ft.TextField(
            width=350,
            bgcolor=ft.colors.WHITE,
            hint_text="Search",
            color=ft.colors.BLACK,
            autofocus=True,  # Set autofocus to True
            on_submit=lambda e: self.search_user_query(e, page, results_instance),  # Trigger search on Enter key press
        )
        self.search_button = ft.IconButton(
            icon=ft.icons.SEARCH,
            icon_size=30,
            tooltip="Search on Libgen",
            on_click=lambda e: self.search_user_query(e, page, results_instance),
        )
        self.loading_icon = ft.ProgressRing()
        self.loading_icon.visible = False

        self.search_area = ft.Container(
            content=ft.Row(
                controls=[self.query_type, self.user_query, self.search_button, self.loading_icon],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )

    def search_user_query(self, e, page, results_instance):
        self.loading_icon.visible = True  # Show loading icon
        page.update()

        s = LibgenSearch()
        if not self.user_query.value:
            self.user_query.error_text = "Invalid query"
            self.loading_icon.visible = False  # Hide loading icon on error
            page.update()
            return

        library_location = page.client_storage.get("library")
        query = self.user_query.value
        query_type = self.query_type.value

        if query_type == "Title":
            query_results = s.search_title(query)
        elif query_type == "Author":
            query_results = s.search_author(query)
        else:
            self.user_query.error_text = "Invalid query type"
            self.loading_icon.visible = False  # Hide loading icon on error
            page.update()
            return

        results_instance.populate_results(query_results, page, library_location)
        self.loading_icon.visible = False  # Hide loading icon when results are ready
        page.update()