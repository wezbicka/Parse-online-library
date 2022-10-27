import os
import argparse
import sys
import logging
from time import sleep

from urllib.parse import urljoin, urlsplit, unquote
import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def fetch_book_id():
    parser = argparse.ArgumentParser(
        description='Скрипт для скачивания книг с сайта tululu.org'
    )
    parser.add_argument(
        '-s',
        '--start_id',
        help='ID, с которого надо скачивать книги',
        default=1,
        type=int
    )
    parser.add_argument(
        '-e',
        '--end_id',
        help='ID, до которого надо скачивать книги',
        default=10,
        type=int
    )
    args = parser.parse_args()
    start_id = args.start_id
    end_id = args.end_id
    return start_id, end_id


def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError


def download_txt(url, payload, filename, folder='books/'):
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, sanitize_filename(f"{filename}.txt"))
    response = requests.get(url, params=payload)
    response.raise_for_status()
    check_for_redirect(response)
    with open(filepath, 'wb') as file:
        file.write(response.content)
    return filepath


def download_image(url, filename, folder='images/'):
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, sanitize_filename(f"{filename}"))
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    with open(filepath, 'wb') as file:
        file.write(response.content)
    return filepath


def parse_book_page(html, base_url):
    soup = BeautifulSoup(html, 'lxml')
    title_tag = soup.find('h1')
    book_title, book_author = title_tag.text.split("::")
    image_tag = soup.find('div', class_='bookimage')
    image_url = urljoin(base_url, image_tag.find('img')['src'])
    comments_tag = soup.find_all('div', class_='texts')
    comments = [comment_tag.find('span', class_='black').text 
                for comment_tag in comments_tag]
    genre_tags = soup.find('span', class_='d_book').find_all("a")
    genres = [tag.text for tag in genre_tags]
    return {
        "title": book_title.strip(),
        "author": book_author.strip(),
        "image": image_url,
        "comments": comments,
        "genres": genres,
    }


def handle_errors(func_, *args):
    first_reconnection = True
    while True:
        try:
            response = func_(*args)

            if not first_reconnection:
                print('Connection is restored.')

            return response

        except requests.exceptions.HTTPError:
            logging.warning(f"Redirect. The book {book_id} not found")
            print(
                f'Книги №{book_id} не найдена!',
                file=sys.stderr
            )
            sys.exit("Error!")
        except requests.ConnectionError as connect_err:
            if first_reconnection:
                print('Connection is down!')
                print(logging.warning(connect_err), file=sys.stderr)
                print('Retry in 5 seconds')
                sleep(5)
                first_reconnection = False
            else:
                print(
                    logging.warning('Connection is still down!'),
                    file=sys.stderr
                    )
                print('Retry in 15 seconds')
                sleep(15)


def download_books_and_images(book_indexes):
    parsed_books = []
    for book_id in book_indexes:
        parsed_books.append(
            handle_errors(
                parse_book_page,
                book_id
            )
        )
        url = f"https://tululu.org/b{book_id}/"
        response = requests.get(url)
        response.raise_for_status()
        check_for_redirect(response)
        book = parse_book_page(response.text, response.url)
        book_title = book['title']
        url_image = book['image']
        print("Заголовок:", book_title)
        print(url_image)
        filename = f'{book_id}. {book_title}'
        print(book['comments'])
        payload = {"id": book_id}
        download_url = f'https://tululu.org/txt.php'
        download_txt(download_url, payload, filename)
        filename = unquote(urlsplit(url_image).path).split("/")[-1]
        print(filename)
        download_image(url_image, filename)

if __name__ == "__main__":
    logging.basicConfig(filename='error.log', filemode='w')
    start_id, end_id = fetch_book_id()
    book_indexes = range(start_id, end_id + 1)
    download_books_and_images(book_indexes)