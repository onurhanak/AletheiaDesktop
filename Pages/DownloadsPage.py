import flet as ft
import threading
import time

class DownloadsPage:
    def __init__(self, page: ft.Page, download_progress):
        self.page = page

        self.download_progress = download_progress
        #self.page.on_resize = self.on_window_resize
        self.downloads_view = ft.Column(expand=1)  
        self.heading_text = ft.Text(
                value="Downloads",  # Replace with your desired heading
                size=25,  # Font size
                weight="bold",  # Font weight
                text_align="center",
            )
        self.content_column = ft.Column(
            controls=[self.heading_text, self.downloads_view],
            alignment=ft.MainAxisAlignment.CENTER,  # Center align the column vertically
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Center align the column horizontally
            expand=1,
        )
        self.downloads_layout = ft.Container(
            content=self.content_column,
            #bgcolor=ft.colors.GREY,
            height=page.window_height * 0.90,
            width=page.window_width * 0.90,
        )

        self.ui_lock = threading.Lock()

        self.update_thread = threading.Thread(target=self.update_ui)
        self.update_thread.start()
    def update_ui(self):
        while True:
            # Acquire lock and update UI (consider thread safety here)
            with self.ui_lock:
                self.downloads_view.controls.clear()

                current_progress = self.download_progress.copy()

                for book_title, progress in current_progress.items():
                    download_item = ft.ListTile(
                        leading=ft.Icon(ft.icons.DOWNLOADING),
                        title=ft.Text(book_title, size=15),  
                        subtitle=ft.Text(f"Progress: {progress}%", size=15),
                    )
                    # Add download_item to downloads_view
                    self.downloads_view.controls.append(download_item)

                self.page.update()

            time.sleep(1) 


    def render(self):
        return self.downloads_layout

    def stop_update_thread(self):
        pass
