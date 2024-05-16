import json
import os
import subprocess
import sys
from pathlib import Path
import gevent
import threading

import eel
import requests
import tkinter as tk
from tkinter import filedialog
from libgen_api_enhanced import LibgenSearch

eel.init("./static")

USER_HOME_DIR = str(Path.home())
DEFAULT_LIBRARY = f"{USER_HOME_DIR}/AletheiaLibrary"
SETTINGS_FILE = f"{USER_HOME_DIR}/.aletheia"


def check_first_run():
    return not os.path.exists(SETTINGS_FILE)


@eel.expose
def get_library_location():
    try:
        with open(SETTINGS_FILE, 'r') as file:
            records = json.load(file)
        return records['download_path']
    except Exception as e:
        eel.showNotification(f"Error reading settings: {e}")


@eel.expose
def save_settings(download_path):
    settings = {
        'download_path': f"{download_path}/AletheiaLibrary",
        "downloads": [],
        "favorites": []
    }
    try:
        with open(SETTINGS_FILE, 'w') as file:
            json.dump(settings, file)
        os.makedirs(settings['download_path'], exist_ok=True)
        eel.redirect()
    except Exception as e:
        eel.showNotification(f"Error saving settings: {e}")


@eel.expose
def select_directory():
    root = tk.Tk()
    root.withdraw()
    directory_path = filedialog.askdirectory()
    save_settings(download_path=directory_path)


def update_records(book, download):
    try:
        with open(SETTINGS_FILE, 'r') as file:
            records = json.load(file)
        if download:
            records["downloads"].append(book)
        else:
            records["favorites"].append(book)
        with open(SETTINGS_FILE, 'w') as file:
            json.dump(records, file)
    except Exception as e:
        eel.showNotification(f"Error updating records: {e}")


@eel.expose
def open_file_with_default_program(book_title):
    try:
        with open(SETTINGS_FILE, 'r') as file:
            records = json.load(file)
        file_path = next(book["file_path"] for book in records['downloads'] if book['Title'] == book_title)

        if sys.platform == "win32":
            os.startfile(file_path)
        elif sys.platform == "darwin":
            subprocess.run(["open", file_path])
        else:
            subprocess.run(["xdg-open", file_path])
    except Exception as e:
        eel.showNotification(f"Error opening file {book_title}: {e}")


@eel.expose
def favorite_book(book):
    try:
        with open(SETTINGS_FILE, 'r') as file:
            settings = json.load(file)
        settings['favorites'].append(book)
        with open(SETTINGS_FILE, 'w') as file:
            json.dump(settings, file)
    except Exception as e:
        eel.showNotification(f"Error saving favorite book: {e}")


@eel.expose
def return_library_elements(library):
    try:
        with open(SETTINGS_FILE, 'r') as file:
            settings = json.load(file)
        return settings['downloads'] if library else settings['favorites']
    except Exception as e:
        eel.showNotification(f"Error retrieving library elements: {e}")


search = LibgenSearch()

@eel.expose
def search_books(query, query_type):
    try:
        if query_type == "title":
            return search.search_title(query)
        elif query_type == "author":
            return search.search_author(query)
    except Exception as e:
        eel.showNotification(f"Error searching books: {e}")


def download_book(book):
    try:
        download_link = book["Direct_Download_Link"]
        book_title = book["Title"]
        book_extension = book["Extension"]
        book_author = book["Author"]

        response = requests.get(download_link, stream=True)
        response.raise_for_status()

        with open(SETTINGS_FILE, 'r') as file:
            settings = json.load(file)

        save_path = settings['download_path']
        file_path = os.path.join(save_path, f"{book_title}.{book_extension}")
        book['file_path'] = file_path

        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        eel.showNotification(f"{book_title} by {book_author} downloaded successfully.")
        update_records(book, True)
    except requests.RequestException as e:
        print(e)
        eel.showNotification(f'Failed to download {book_title}: {e}')
    except Exception as e:
        print(e)
        eel.showNotification(f'Failed to download {book_title}: {e}')



@eel.expose
def unfavorite_book(book_title):

    try:
        with open(SETTINGS_FILE, 'r') as file:
            settings = json.load(file)

        settings['favorites'] = [book for book in settings['favorites'] if book['Title'] != book_title]
        
        with open(SETTINGS_FILE, 'w') as file:
            json.dump(settings, file)

        eel.showNotification(f'Removed {book_title} from favorites.')
    except Exception as e:
        eel.showNotification(f'Failed to remove {book_title} from favorites : {e}')

@eel.expose
def delete_book(book_title):

    try:
        with open(SETTINGS_FILE, 'r') as file:
            settings = json.load(file)

        to_delete = [book['file_path'] for book in settings['downloads'] if book['Title'] == book_title][0]
        
        os.remove(to_delete)

        settings['downloads'] = [book for book in settings['downloads'] if book['Title'] != book_title]
        
        with open(SETTINGS_FILE, 'w') as file:
            json.dump(settings, file)

        eel.showNotification(f'Deleted {book_title}')
    except Exception as e:
        eel.showNotification(f'Failed to delelete {book_title} : {e}')


@eel.expose
def download_book_thread(book):
    download_thread = threading.Thread(target=download_book, args=(book,))
    download_thread.start()

def start_app():
    if check_first_run():
        eel.start('welcome.html', block=False, mode="chrome")
        gevent.get_hub().join()
    else:
        eel.start('splash.html', block=False, mode="chrome")
        gevent.get_hub().join()

if __name__ == '__main__':
    start_app()