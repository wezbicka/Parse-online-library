import os

import requests


def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError


if __name__ == "__main__":
    directory = "books"
    os.makedirs(directory, exist_ok=True)
    for id in range(1, 11):
        url = f"https://tululu.org/txt.php?id={id}"
        response = requests.get(url)
        response.raise_for_status()
        try:
            check_for_redirect(response)
        except requests.exceptions.HTTPError:
            continue

        filename = f'id{id}.txt'
        with open(os.path.join(directory, filename), 'wb') as file:
            file.write(response.content)
