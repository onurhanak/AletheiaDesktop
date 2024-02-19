import flet as ft
import threading
import time

class DownloadsPage:
    def __init__(self, page: ft.Page, download_progress):
        self.page = page
        self.download_progress = download_progress  # Shared dictionary for tracking download progress
        self.downloads_view = ft.Column(expand=1)  # Use a Column for dynamic updates

        # Title for the Downloads page
        title = ft.Text("In-Progress Downloads", size=32, weight=ft.FontWeight.BOLD, text_align="center", color=ft.colors.BLUE)

        # Overall layout
        self.downloads_layout = ft.Column(
            controls=[
                title,
                self.downloads_view
            ],
            expand=1,
            spacing=12,
            #alignment=ft.MainAxisAlignment.CENTER,
            #horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        # Start a thread to periodically update the UI
        self.update_thread = threading.Thread(target=self.update_ui)
        self.update_thread.start()

    def update_ui(self):
        while True:
            # Safely stop this thread as needed
            # Clear the downloads view for updated progress bars
            self.downloads_view.controls.clear()
            for book_title, progress in self.download_progress.items():
                # Create a progress bar for each book
                pb = ft.ProgressBar(value=progress, width=self.page.width, height=5)
                book_info = ft.Text(f"{book_title} - Progress: {progress}%", size=12)
                progress_bar = ft.Column([book_info, pb], spacing=5)
                divider = ft.Divider(color=ft.colors.GREY)
                self.downloads_view.controls.extend([progress_bar, divider])
            self.page.update()
            time.sleep(1)  # Update interval; adjust as needed

    def render(self):
        return self.downloads_layout

    def stop_update_thread(self):
        # Implement stopping mechanism for the update thread
        pass
