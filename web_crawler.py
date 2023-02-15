import requests
from bs4 import BeautifulSoup
import os

# конфигурационные переменные
# сайт для получения ссылок
MAIN_LINK = 'https://genius.com/tags/russian-hyperpop/all?page='
# количество нужных ссылок
COUNT_PAGES = 100
# файл для сохранения информации о ссылке и файла "выкачки"
INFO_FILE = 'index.txt'


def get_links(url):
    page = requests.get(url)
    data = page.text
    soup = BeautifulSoup(data, features="lxml")
    links = []
    for item in soup.select("a.song_link"):
        links.append(item['href'])
    return links


# Функция для удаления html-тегов
def remove_tags(html):
    soup = BeautifulSoup(html, "html.parser")
    for data in soup(['style', 'script', 'noscript', 'link']):
        # Удаление тегов
        data.decompose()
    return str(soup)


def crawl(url):
    page = requests.get(url)
    data = page.text
    return remove_tags(data)


if __name__ == '__main__':
    links_all = []
    i = 1
    info_string = ""
    while len(links_all) < COUNT_PAGES:
        current_link = f'{MAIN_LINK}{i}'
        links = get_links(current_link)
        links_all += links
        i += 1
    for i, link in enumerate(links_all):
        html_text = crawl(link)
        filename = f'00{i}' if i < 10 else f'0{i}'
        info_string += f"{filename}\t{link}\n"
        path_result = f"Выкачка/{filename}.txt"
        os.makedirs(os.path.dirname(path_result), exist_ok=True)
        with open(path_result, "w", encoding="utf-8") as file_result:
            file_result.write(html_text)
    with open(INFO_FILE, "w", encoding="utf-8") as f:
        f.write(info_string)
