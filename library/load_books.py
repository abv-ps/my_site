"""
Script for loading test data into the Library API.

This script uses the 'requests' library to send POST requests to the API
to create books in the database. It utilizes an authorization token for
accessing the API.

Example usage:
    python load_test_data.py

Dependencies:
    requests
    json
"""
import requests
import json

url = 'http://127.0.0.1:8000/api/books/'
access_token = 'YOUR_ACCESS_TOKEN'


books = [
    {"title": "Тіні забутих предків", "author": "Михайло Коцюбинський", "genre": "Проза", "publication_year": 1911},
    {"title": "Лісова пісня", "author": "Леся Українка", "genre": "Драма", "publication_year": 1912},
    {"title": "Майстер корабля", "author": "Юрій Яновський", "genre": "Роман", "publication_year": 1928},
    {"title": "Місто", "author": "Валер'ян Підмогильний", "genre": "Роман", "publication_year": 1928},
    {"title": "Зачарована Десна", "author": "Олександр Довженко", "genre": "Автобіографічна проза", "publication_year": 1956},
    {"title": "Собор", "author": "Олесь Гончар", "genre": "Роман", "publication_year": 1968},
    {"title": "Дім на горі", "author": "Валерій Шевчук", "genre": "Роман", "publication_year": 1983},
    {"title": "Музей покинутих секретів", "author": "Оксана Забужко", "genre": "Роман", "publication_year": 2009},
    {"title": "Записки українського самашедшого", "author": "Ліна Костенко", "genre": "Роман", "publication_year": 2010},
    {"title": "Ворошиловград", "author": "Сергій Жадан", "genre": "Роман", "publication_year": 2010},
    {"title": "Інтернат", "author": "Сергій Жадан", "genre": "Роман", "publication_year": 2017},
    {"title": "Фелікс Австрія", "author": "Софія Андрухович", "genre": "Роман", "publication_year": 2014},
    {"title": "Доця", "author": "Тамара Горіха Зерня", "genre": "Роман", "publication_year": 2019},
    {"title": "Танго смерті", "author": "Юрій Винничук", "genre": "Роман", "publication_year": 2012},
    {"title": "Добрий Бог не покине", "author": "Ірина Цілик", "genre": "Роман", "publication_year": 2021},
]

headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json',
}

for book in books:
    response = requests.post(url, headers=headers, data=json.dumps(book))
    if response.status_code == 201:
        print(f'Книга "{book["title"]}" успішно завантажена.')
    else:
        print(f'Помилка завантаження книги "{book["title"]}": {response.status_code} - {response.text}')