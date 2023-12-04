import time

from flask import Flask, request
import requests

GOOGLE_BOOKS_URL = 'https://www.googleapis.com/books/v1/volumes?q={}'
OPEN_LIBRARY_ISBN = 'https://openlibrary.org/isbn/{}.json'
OPEN_LIBRARY_RATINGS = 'https://openlibrary.org/{}/ratings.json'
PORT = 12345


def get_open_library_data(isbn: str) -> dict:
    """
    Retrieves a book's ratings on the Open Library platform.
    :param isbn: Book's ISBN.
    :return: dictionary of data if positive results, else None. Dictionary formatted as:
    {
        'counts': {'1': int, '2': int, '3': int, '4': int, '5': int},
        'summary': {'average': int | None, 'count': int}
    }
    """

    isbn_data = requests.get(OPEN_LIBRARY_ISBN.format(isbn))
    if isbn_data.status_code != 200:
        return {}
    isbn_data_json = isbn_data.json()
    open_library_works = isbn_data_json.get('works')
    if not open_library_works:
        return {}
    open_library_works_key = open_library_works[0].get('key')
    open_library_ratings = requests.get(OPEN_LIBRARY_RATINGS.format(open_library_works_key))
    open_library_ratings_json = open_library_ratings.json()

    return open_library_ratings_json


def get_google_results(search_query: str) -> dict:
    """
    Retrieves Google Books API results.
    :param search_query: Query term.
    :return: JSON of Google results.
    """
    google_data = requests.get(GOOGLE_BOOKS_URL.format(search_query))
    google_data_json = google_data.json()
    return google_data_json


def create_app():
    app = Flask(__name__)

    @app.route('/retrieve-book-data', methods=['POST'])
    def retrieve_book_data():
        request_data = request.data.decode()
        return_data = get_google_results(request_data)
        if return_data.get('totalItems') == 0 or return_data.get('totalItems') is None:
            return {}

        for book in return_data['items']:
            book['openLibrary'] = {}
            book['nyTimes'] = {}
            if isbn := book.get('volumeInfo').get('industryIdentifiers')[0].get('identifier'):
                open_library_data = get_open_library_data(isbn)
                if open_library_data and open_library_data.get('summary').get('count') > 0:
                    book['openLibrary'].update(open_library_data)

        return return_data['items']

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(port=PORT)
