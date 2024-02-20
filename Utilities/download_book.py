import flet as ft
import threading
import requests
from Utilities.notify import create_notification

def get_downloaded_books(page):
    books = page.client_storage.get("downloaded_books")
    if books is None:
        return []
    return books


def update_library(page, book, file_path):
    already_downloaded_books = get_downloaded_books(page)

    if not isinstance(book, dict):
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
    else:
        book["file_path"] = file_path
        book_dict = book

    if book_dict not in already_downloaded_books:
        already_downloaded_books.append(book_dict)
        page.client_storage.set("downloaded_books", already_downloaded_books)


def download_book_from_favorites(book, library_location, page, download_progress):

    def download():
        create_notification(f"{book.title}", "Starting download")


        download_url = book.download_link
        file_path = f"{library_location}/{book.title}-{book.author}.{book.filetype}"

        try:
            response = requests.get(download_url, stream=True)
            if response.status_code == 200:
                total_length = response.headers.get("content-length")

                if total_length is None:
                    with open(file_path, "wb") as file:
                        file.write(response.content)
                else:
                    dl = 0
                    total_length = int(total_length)
                    with open(file_path, "wb") as file:  # 4096 *
                        for data in response.iter_content(chunk_size=4096):
                            dl += len(data)
                            file.write(data)
                            done = int(100 * dl / total_length)
                            download_progress[book.title] = done
                            page.update()

                completion_message = [book.title, "Download successful."]
                update_library(page, book, file_path)
            else:
                completion_message = [book.title, "Download failed."]

        except Exception as e:
                completion_message = [book.title, f"Download failed. Error: {e}"]

        create_notification(completion_message[0], create_notification[1])


    threading.Thread(target=download).start()


def download_book(book, library_location, page, download_progress):

    def download():
        create_notification(f"{book.title}", "Starting download")

        download_url = book.download_link
        file_path = f"{library_location}/{book.title}-{book.author}.{book.filetype}"

        try:
            response = requests.get(download_url, stream=True)
            if response.status_code == 200:
                total_length = response.headers.get("content-length")

                if total_length is None:
                    with open(file_path, "wb") as file:
                        file.write(response.content)
                else:
                    dl = 0
                    total_length = int(total_length)
                    with open(file_path, "wb") as file:
                        for data in response.iter_content(chunk_size=4096):
                            dl += len(data)
                            file.write(data)
                            done = int(100 * dl / total_length)
                            download_progress[book.title] = done
                            page.update()

                completion_message = [book.title, "Download successful."]
                update_library(page, book, file_path)
            else:
                completion_message = [book.title, "Download failed."]

        except Exception as e:
            completion_message = [book.title, f"Download failed. Error: {e}"]

        create_notification(completion_message[0], create_notification[1])

    threading.Thread(target=download).start()
