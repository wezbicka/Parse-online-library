import os

import requests


# url = "https://dvmn.org/filer/canonical/1542890876/16/"

# response = requests.get(url)
# response.raise_for_status() 

# filename = 'dvmn.svg'
# with open(filename, 'wb') as file:
#     file.write(response.content)
if __name__ == "__main__":
    directory = "books"
    if not os.path.exists(directory):
        os.makedirs(directory)

    url = "https://tululu.org/txt.php?id=32168"
    response = requests.get(url)
    response.raise_for_status() 

    filename = 'book.txt'
    with open(filename, 'wb') as file:
        file.write(response.content)
