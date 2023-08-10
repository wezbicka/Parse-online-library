import requests
from bs4 import BeautifulSoup

from urllib.parse import urljoin


url = 'https://tululu.org/l55/'
response = requests.get(url)
response.raise_for_status()
soup = BeautifulSoup(response.text, 'lxml')
book_id = soup.find("div", class_="bookimage").find("a")["href"]
book_url = urljoin(url, book_id)
print(book_url)
