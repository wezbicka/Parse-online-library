import os
from urllib.parse import urljoin

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
    with open(filepath, 'wb') as file:
        file.write(response.content)
    return filepath


def parse(response):
    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find('h1')
    book_title, author_book = title_tag.text.split("::")
    image_tag = soup.find('div', class_='bookimage')
    image_url = urljoin('https://tululu.org', image_tag.find('img')['src'])
    return {
        "title": book_title.strip(),
        "author": author_book.strip(),
        "image": image_url,
    }


if __name__ == "__main__":
    for id in range(1, 11):
        try:
            download_url = f'https://tululu.org/txt.php?id={id}'
            response = requests.get(download_url)
            response.raise_for_status()
            check_for_redirect(response)
        except requests.exceptions.HTTPError:
            continue

        url = f"https://tululu.org/b{id}/"
        response = requests.get(url)
        response.raise_for_status()
        book = parse(response)
        print("Заголовок:", book['title'])
        print(book['image'])
        print()
        filename = f'{id}. {book["title"]}'
        download_txt(download_url, filename)
