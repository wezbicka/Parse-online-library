import os

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError


def download_txt(url, filename, folder='books/'):
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, sanitize_filename(f"{filename}.txt"))
    response = requests.get(url)
    response.raise_for_status()
    try:
        check_for_redirect(response)
    except requests.exceptions.HTTPError:
        return
    with open(filepath, 'wb') as file:
        file.write(response.content)
    return filepath


def parse(response):
    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find('h1')
    book_title, *author_book = title_tag.text.split("::")
    return {
        "title": book_title.strip(),
        "author": author_book,
    }


if __name__ == "__main__":
    for id in range(1, 11):
        url = f"https://tululu.org/b{id}/"
        response = requests.get(url)
        response.raise_for_status()
        book = parse(response)
        print(book['title'], book['author'])
        download_url = f'https://tululu.org/txt.php?id={id}'
        filename = f'{id}. {book["title"]}'
        download_txt(download_url, filename)
