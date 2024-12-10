# Парсер Citilink

Парсит общие характеристики товара с страницы (название, категория, цена, ссылка на изображение, рейтинг, количество отзывов, описание (если пустое, то плейсхолдерное описание)) и сохраняет их в файл формата JSON.

## Выбор парсируемых категорий  

Парсер просматривает по умолчанию 2 страницы каждой категории, указанной в `urls_to_parse`. Чтобы указать свои категории, измените ссылки в `urls_to_parse` на свои. Пример,
```python
urls_to_parse = [
         'https://www.citilink.ru/catalog/processory/?p=',
         'https://www.citilink.ru/catalog/ssd-nakopiteli/?p=',
         'https://www.citilink.ru/catalog/noutbuki/?p=',
     ] # ?p= обязательно!, иначе парсер не сможет просмотреть следующие страницы
```
Чтобы выбрать своё количество страниц, которое просмотрит парсер, измените переменную `max_pages_to_parse` на своё значение. Пример,
```python
max_pages_to_parse = 2
```

## Запуск проекта  
Клонируйте проект

~~~bash  
  git clone https://github.com/shirotame/parser-citilink
~~~

Перейдите в папку проекта 

~~~bash  
  cd parser-citilink
~~~

Установите зависимости и, если необходомо, то виртуальное окружение Python

~~~bash  
pip install requirements.txt
~~~

~~~bash
python -m venv
~~~

Запустите проект 

~~~bash  
python main.py
~~~  

Результат работы будет находится в директории проекта в папке result в формате json файлов
~~~bash
cd result
~~~