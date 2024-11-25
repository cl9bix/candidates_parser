import urllib.parse

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.work.ua/resumes/by-category/"


def fetch_categories():
    response = requests.get(BASE_URL)
    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    categories = []

    category_list = soup.find_all("li", class_="no-style mb-md")
    for c in category_list:
        link_element = c.find("a", class_="link-inverse")
        if link_element:
            name = link_element.text.strip()
            url = f"https://www.work.ua{link_element['href']}"
            categories.append({"name": name, "url": url})
    return categories


import requests
from bs4 import BeautifulSoup
import urllib.parse


def parse_with_filters(filters: dict):
    base_url: str = "https://www.work.ua/resumes"
    print("Запит з фільтрами:", filters)

    query_params = {}

    # Формуємо частину URL для позиції (якщо є)
    position = filters.get('position')
    if position:
        # Якщо позиція є, додаємо її до основного URL
        position_part = f"-{position.replace(' ', '+')}"
    else:
        position_part = ''

    # Перевірка та додавання інших фільтрів до параметрів запиту
    if filters.get('experience'):
        query_params['experience'] = filters['experience']

    if filters.get('preoccupancy'):
        query_params['employment'] = filters['preoccupancy']

    if filters.get('salary_from'):
        query_params['salaryfrom'] = filters['salary_from']

    if filters.get('salary_to'):
        query_params['salaryto'] = filters['salary_to']  # Максимальна зарплата

    # Формуємо фінальний URL
    final_url = f"{base_url}{position_part}/"

    # Якщо є додаткові фільтри, додаємо їх як параметри запиту
    if query_params:
        query_string = urllib.parse.urlencode(query_params, doseq=True)
        final_url = f"{final_url}?{query_string}"

    print(f"Запит за URL: {final_url} з параметрами: {query_params}")

    try:
        response = requests.get(final_url)

        if response.status_code != 200:
            print(f"Помилка: {response.status_code} під час запиту на {final_url}")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        data = []

        data_list = soup.find_all("div", class_="mt-sm")
        for i in data_list:
            link_element = i.find("a", href=True)
            if link_element:
                name = link_element.text.strip()
                url = f"https://www.work.ua{link_element['href']}"
                data.append({"name": name, "url": url})

        print(data)
        return data

    except Exception as e:
        print(f"Сталася помилка: {e}")
        return []
