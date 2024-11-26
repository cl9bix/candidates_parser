import requests
import urllib.parse
from bs4 import BeautifulSoup
from src.bot.cfg import city_translations, exp_dct

BASE_URL = "https://www.work.ua/resumes"


def fetch_categories():
    response = requests.get(BASE_URL)
    if response.status_code != 200:
        print(f"Помилка: {response.status_code}")
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


def parse_with_filters(filters: dict):
    print("Запит з фільтрами:", filters)

    location_part = ""
    if filters.get('location'):
        city_name = filters['location']
        location_part = city_translations.get(city_name, city_name).lower()

    position_part = ""
    if filters.get('position'):
        position_part = filters['position'].replace(' ', '+').lower()

    if location_part:
        base_url = f"{BASE_URL}-{location_part}-{position_part}" if position_part else f"{BASE_URL}-{location_part}"
    else:
        base_url = f"{BASE_URL}-{position_part}" if position_part else BASE_URL

    query_params = {}

    if filters.get('experience'):
        experience_value = filters['experience']
        key = None
        for k, v in exp_dct.items():
            if v == experience_value:
                key = k
                break
        if key:
            query_params['experience'] = key

    if filters.get('preoccupancy'):
        lst = ['не повна', 'неповна']
        data = filters['preoccupancy']
        if data.lower() == 'повна':
            query_params['employment'] = 74
        elif data.lower() in lst:
            query_params['employment'] = 75

    if filters.get('salary_from'):
        query_params['salaryfrom'] = filters['salary_from']

    if filters.get('salary_to'):
        query_params['salaryto'] = filters['salary_to']

    if query_params:
        query_string = urllib.parse.urlencode(query_params, doseq=True)
        final_url = f"{base_url}/?{query_string}"
    else:
        final_url = base_url

    print(f"Запит за URL: {final_url}")

    try:
        response = requests.get(final_url)

        if response.status_code != 200:
            print(f"Помилка: {response.status_code} під час запиту на {final_url}")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        data = []

        data_list = soup.find_all("div", class_="mt-sm")
        if not data_list:
            print(f"Не вдалося знайти елементи за запитом: {final_url}")
            return []

        for i in data_list:
            link_element = i.find("a", href=True)
            if link_element:
                resume_url = link_element['href']
                if resume_url.startswith('/resumes/'):
                    resume_url = f"https://www.work.ua{resume_url}"
                    name = link_element.text.strip()
                    data.append({"name": name, "url": resume_url})

        print(f"Знайдено {len(data)} резюме")
        # print(data)
        return data

    except Exception as e:
        print(f"Сталася помилка: {e}")
        return []
