import os

import requests


if __name__ == "__main__":
    directory = "books"
    os.makedirs(directory, exist_ok=True)
    for id in range(10):
        url = f"https://tululu.org/txt.php?id={id + 1}"
        response = requests.get(url)
        response.raise_for_status() 

        filename = f'book{id}.txt'
        with open(os.path.join(directory, filename), 'wb') as file:
            file.write(response.content)
