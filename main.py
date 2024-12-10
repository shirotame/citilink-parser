from json import dumps
from typing import Any, Iterable, Mapping, Optional
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

max_pages_to_parse = 2

urls_to_parse = [
         'https://www.citilink.ru/catalog/processory/?p=',
         'https://www.citilink.ru/catalog/videokarty/?p=',
         'https://www.citilink.ru/catalog/ssd-nakopiteli/?p=',
         'https://www.citilink.ru/catalog/noutbuki/?p=',
         'https://www.citilink.ru/catalog/smartfony/?p=',
         'https://www.citilink.ru/catalog/materinskie-platy/?p=',
     ]

categories = [
    'Процессор',
    'Ноутбук',
    'SSD накопитель',
    'Видеокарта',
    'Смартфон',
    'Материнская плата'
]

def __main__():
    file_urls = []
    try:
         with open("urls.txt", mode="r") as file:
            print("Найден файл с кэшированными ссылками, используем их")
            file_urls = file.read().split('\n')[0:-1]
    except FileNotFoundError: 
        print("Кэшированных ссылок нет, начинаем с начала")

    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=True, devtools=True)
        page = browser.new_page()

        urls = []
        if len(file_urls) == 0:
            for url in urls_to_parse:
                pg = 1
                page.goto(url=f'{url}{pg}')

                while pg != max_pages_to_parse + 1:
                    page.wait_for_timeout(1200)
                    page_urls = get_urls_from_page(page)
                    print(f'Страница {page}')

                    urls.extend(page_urls)

                    pg += 1

                    page.goto(f'{url}{pg}')

            with open("urls.txt", mode="w") as file:
                for u in urls:
                    file.write(f'{u}\n')
        else:
            urls = file_urls
        print(len(urls))

        items = []
        for i, item in enumerate(urls, start=1):
            page.goto(url=item)
            page.wait_for_load_state('domcontentloaded')
            if 'captcha' in page.url:
                print("Парсер словил капчу, перезапустите проект, предварительно удалив первые n строк. (n - число, которое вывелось в консоль самым последним)")
                break
            items.append(get_data(page))
            print(f"Информация с сайта {i} получена") 

        to_json(items, file_name=f"items")

        page.close() 

def get_urls_from_page(page) -> list[str]:
    """get_urls_from_page

        Получает все товары с текущей страницы.

        Returns
        -------
        list[str] - список всех ссылок на товары
        """
    soup = BeautifulSoup(page.content(), 'lxml')
    elements = soup.find_all('a', class_="app-catalog-9gnskf e1259i3g0")
    return list(map(
        lambda element: 'https://www.citilink.ru' + element.get("href"),
        elements
    ))

def format_name(name: str) -> str:
    if not name.endswith('а'):
        return name
    newstr = name[0:-1] + 'у'
    return newstr
    

def get_data(page) -> dict[str, str | int]:
    """get_urls_from_page

        Парсит определённые характеристики товара с страницы (название, категория, цена, ссылка на изображение, рейтинг, количество отзывов, описание (если пустое, то плейсхолдерное описание)).

        Returns
        -------
        dict[str, str | int] - словарь характеристик ('название характеристики': параметр)
        """
    soup = BeautifulSoup(page.content(), 'lxml')
    title =soup.find('h1', class_ = "easmdi50 eml1k9j0 app-catalog-lc5se5 e1gjr6xo0").text.replace('Характеристики ', '')
    title_splitted = title.split(' ')

    category = title_splitted[0]
    name = title.split(',')[0].replace(category + ' ', '')

    price = 0 if soup.find('span', class_="e1j9birj0 e106ikdt0 app-catalog-8hy98m e1gjr6xo0") is None else soup.find('span', class_="e1j9birj0 e106ikdt0 app-catalog-8hy98m e1gjr6xo0").text.replace(' ', '')
    img = soup.find('img', class_="ekkbt9g0 app-catalog-15kpwh2 e1fcwjnh0", alt=f"{title}").attrs['src']
    rating = 0 if soup.find('div', class_="e8eovjk0 app-catalog-1uwfsq8 e2kybqa2") is None else soup.find('div', class_="e8eovjk0 app-catalog-1uwfsq8 e2kybqa2").text
    reviews_count = 0 if soup.find('div', class_="e8eovjk0 app-catalog-3ygtq1 e2kybqa2") is None else soup.find('div', class_="e8eovjk0 app-catalog-3ygtq1 e2kybqa2").text.split(' ')[0]
    descr = f'В нашем маркетплейсе вы можете приобрести {format_name(category.lower())} {name} по низкой цене.' if soup.find('div', class_="app-catalog-8zawkn e1qcmsu70") is None else soup.find('div', class_="app-catalog-8zawkn e1qcmsu70").findChildren('p')[0].text

    data = {
        'name': name,
        'category': category,
        'price': int(price),
        'img': img,
        'rating': float(rating),
        'reviews_count': int(reviews_count),
        'descr': descr
    }
    return data

def to_json(data: Iterable[Mapping[str, Any]],
            file_name: Optional[str] = "data") -> None:
    """
    Создаёт из итерируемого объекта json файл в папке "result".
    """
    with open(f'result/{file_name}.json', 'w', encoding='utf-8') as file:
        file.write(dumps(data, indent=4, ensure_ascii=False))


if __name__ == '__main__':
    __main__()
