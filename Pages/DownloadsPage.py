import flet as ft
import threading
import time

class DownloadsPage:
    def __init__(self, page: ft.Page, download_progress):
        self.page = page

        self.download_progress = download_progress
        self.downloads_view = ft.Column(expand=1)  
        self.ui_lock = threading.Lock()

        #title = ft.Text("In-Progress Downloads", size=32, weight=ft.FontWeight.BOLD, text_align="center")

        self.downloads_layout = ft.Column(
            controls=[
                #title,
                self.downloads_view
            ],
            expand=1,
            spacing=12,
        )

        self.update_thread = threading.Thread(target=self.update_ui)
        self.update_thread.start()

    def update_ui(self):
        while True:
            with self.ui_lock:
                self.downloads_view.controls.clear()

                current_progress = self.download_progress.copy()

                for book_title, progress in current_progress.items():
                    pb = ft.ProgressBar(value=progress, width=self.page.width/2, height=15)
                    book_info = ft.Text(f"{book_title} - {progress}%", size=15)
                    progress_bar = ft.Column([book_info, pb], spacing=5)
                    self.downloads_view.controls.append(progress_bar)

                self.page.update()

            time.sleep(1) 

    def render(self):
        return self.downloads_layout

    def stop_update_thread(self):
        pass
