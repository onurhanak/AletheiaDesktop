import flet as ft
import threading
import requests


def get_downloaded_books(page):
    books = page.client_storage.get("downloaded_books")
    if books is None:
        return []
    return books


def update_library(page, book, file_path):
    already_downloaded_books = get_downloaded_books(page)

    if type(book) != dict:
        book_dict = {
            "book_id": book.book_id,
            "title": book.title,
            "author": book.author,
            "publisher": book.publisher,
            "year": book.year,
            "pages": book.pages,
            "filetype": book.filetype,
            "cover": book.cover,
            "download_link": book.download_link,
            "file_path": file_path,
        }
    elif type(book) == dict:
        book["file_path"] = file_path
        book_dict = book

    if not book_dict in already_downloaded_books:
        already_downloaded_books.append(book_dict)
        page.client_storage.set("downloaded_books", already_downloaded_books)


def download_book_from_favorites(book, library_location, page):
    def show_bottom_sheet(message):
        bottom_sheet = ft.BottomSheet(
            content=ft.Text(message, size=18),
            dismissible=True,
        )
        page.bottom_sheet = bottom_sheet
        bottom_sheet.open = True
        page.update()

    def download():
        start_message = f"      Starting download of '{book['title']}'...      "
        show_bottom_sheet(start_message)

        download_url = book["download_link"]
        file_path = (
            f"{library_location}/{book['title']}-{book['author']}.{book['filetype']}"
        )

        try:
            response = requests.get(download_url, stream=True)
            if response.status_code == 200:
                with open(file_path, "wb") as file:
                    file.write(response.content)

                completion_message = (
                    f"      '{book['title']}' has been downloaded successfully!      "
                )
                update_library(page, book, file_path)
            else:
                completion_message = f"      Could not download '{book['title']}'      "

        except Exception as e:
            completion_message = f"      Error downloading '{book['title']}': {e}      "

        show_bottom_sheet(completion_message)

    threading.Thread(target=download).start()


def download_book(book, library_location, page):
    def show_bottom_sheet(message):
        bottom_sheet = ft.BottomSheet(
            content=ft.Text(message, size=18),
            dismissible=True,
        )
        page.bottom_sheet = bottom_sheet
        bottom_sheet.open = True
        page.update()

    def download():
        start_message = f"      Starting download of '{book.title}'...      "
        show_bottom_sheet(start_message)

        download_url = book.download_link
        file_path = f"{library_location}/{book.title}-{book.author}.{book.filetype}"

        try:
            response = requests.get(download_url, stream=True)
            if response.status_code == 200:
                with open(file_path, "wb") as file:
                    file.write(response.content)
                completion_message = (
                    f"      '{book.title}' has been downloaded successfully!      "
                )
                show_bottom_sheet(completion_message)
                update_library(page, book, file_path)
            else:
                completion_message = f"      Could not download '{book.title}'      "

        except Exception as e:
            completion_message = f"      Error downloading '{book.title}': {e}      "

        show_bottom_sheet(completion_message)

    threading.Thread(target=download).start()
