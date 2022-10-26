# Парсер книг с сайта tululu.org
Программа для скачивания книг с сайта [tululu.org](https://tululu.org). Функция `download_txt(url, filename, folder='books/')` скачивает книги в формате txt. Также скрипт скачивает обложки книг с сайта с помощью `download_image(url, filename, folder='images/')`. Скрипт выводит названия и авторов книг, комменатрии и жанры.

## Как установить
Python3 должен быть уже установлен. Затем используйте pip (или pip3, есть конфликт с Python2)

Для установки зависимостей:
```
pip install -r requirements.txt
```
## Запуск
```
python tululu.py --start_id 1 --end_id 10
```
Можно использовать сокращенную запись:
```
python tululu.py -s 1 -e 10
```
Можно не указывать параметры `--start_id` и `--end_id`, по умолчанию будут скачиваться страницы от 1 до 10.
В случае успешного выполнения скрипт ничего не выводит.

## Доступные параметры:

`--start_id` - Индекс, начиная с какой страницы скачивать книги. По умолчанию: 1

`--end_id` - Индекс, по какую страницу скачивать книги (включительно). По умолчанию: 10

## Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).