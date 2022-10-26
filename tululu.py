import os
import argparse

from urllib.parse import urljoin, urlsplit, unquote
import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def create_parser():
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


def download_txt(url, filename, folder='books/'):
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, sanitize_filename(f"{filename}.txt"))
    response = requests.get(url)
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


def parse_book_page(html):
    soup = BeautifulSoup(html, 'lxml')
    title_tag = soup.find('h1')
    book_title, book_author = title_tag.text.split("::")
    image_tag = soup.find('div', class_='bookimage')
    image_url = urljoin('https://tululu.org', image_tag.find('img')['src'])
    comments_tag = soup.find_all('div', class_='texts')
    comments = []
    for comment_tag in comments_tag:
        comment = comment_tag.find('span', class_='black').text
        comments.append(comment)
    genre_tags = soup.find('span', class_='d_book').find_all("a")
    genres = []
    for tag in genre_tags: 
        genres.append(tag.text)
    return {
        "title": book_title.strip(),
        "author": book_author.strip(),
        "image": image_url,
        "comments": comments,
        "genres": genres,
    }


if __name__ == "__main__":
    start_id, end_id = create_parser()
    for book_id in range(start_id, end_id + 1):
        try:
            url = f"https://tululu.org/b{book_id}/"
            response = requests.get(url)
            response.raise_for_status()
            check_for_redirect(response)
            book = parse_book_page(response.text)
            book_title = book['title']
            url_image = book['image']
            print("Заголовок:", book_title)
            print(url_image)
            filename = f'{book_id}. {book_title}'
            print(book['comments'])
            download_url = f'https://tululu.org/txt.php?id={book_id}'
            download_txt(download_url, filename)
            filename = unquote(urlsplit(url_image).path).split("/")[-1]
            print(filename)
            download_image(url_image, filename)
        except requests.exceptions.HTTPError:
            continue
        