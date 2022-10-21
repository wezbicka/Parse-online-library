import os

import requests
from bs4 import BeautifulSoup


def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError


def download_book(url, path):
    response = requests.get(url)
    response.raise_for_status()
    try:
        check_for_redirect(response)
    except requests.exceptions.HTTPError:
        return
    with open(path, 'wb') as file:
        file.write(response.content)


if __name__ == "__main__":
    # directory = "books"
    # os.makedirs(directory, exist_ok=True)
    # for id in range(1, 11):
    #     url = f"https://tululu.org/txt.php?id={id}"
        
    #     filename = f'id{id}.txt'
    #     book_path = os.path.join(directory, filename)
    url = "https://tululu.org/b1/"
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find('h1')
    book = title_tag.text.split("::")
    book_title = book[0].strip()
    author_book = book[1].strip()
    print("Заголовок:", book_title)
    print("Автор:", author_book)
