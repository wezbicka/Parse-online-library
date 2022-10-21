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


if __name__ == "__main__":
    # for id in range(1, 11):
    #     url = f"https://tululu.org/txt.php?id={id}"
        
    #     filename = f'id{id}.txt'


    # url = "https://tululu.org/b1/"
    # response = requests.get(url)
    # response.raise_for_status()
    # soup = BeautifulSoup(response.text, 'lxml')
    # title_tag = soup.find('h1')
    # book = title_tag.text.split("::")
    # book_title = book[0].strip()
    # author_book = book[1].strip()
    # print("Заголовок:", book_title)
    # print("Автор:", author_book)


    url = 'https://tululu.org/txt.php?id=1'

    filepath = download_txt(url, 'Алиби')
    print(filepath)  # Выведется books/Алиби.txt

    filepath = download_txt(url, 'Али/би', folder='books/')
    print(filepath)  # Выведется books/Алиби.txt

    filepath = download_txt(url, 'Али\\би', folder='txt/')
    print(filepath)  # Выведется txt/Алиби.txt
