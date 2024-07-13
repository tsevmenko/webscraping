import requests
import re
import json
import sqlite3

def fetch_main_page():
    url = "https://www.lejobadequat.com/emplois"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def extract_vacancies(content):
    job_pattern = re.compile(
        r'<a\s+href="(https://www\.lejobadequat\.com/emplois/[^\"]+)"\s+title="([^"]+)"',
        re.IGNORECASE
    )
    matches = job_pattern.findall(content)
    vacancies = [{"title": match[1], "url": match[0]} for match in matches]
    return vacancies

def store_vacancies_to_json(vacancies, filename):
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(vacancies, json_file, ensure_ascii=False, indent=4)
    print(f"Vacancies stored in {filename}")

def store_vacancies_to_sqlite(vacancies, db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vacancies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            url TEXT
        )
    ''')

    cursor.executemany('''
        INSERT INTO vacancies (title, url)
        VALUES (?, ?)
    ''', [(vacancy['title'], vacancy['url']) for vacancy in vacancies])

    conn.commit()
    conn.close()
    print(f"Vacancies stored in {db_name}")

if __name__ == "__main__":
    content = fetch_main_page()
    if content:
        print("Content fetched successfully.")
        vacancies = extract_vacancies(content)
        if vacancies:
            print(f"Found {len(vacancies)} vacancies:")
            for vacancy in vacancies:
                print(f"Title: {vacancy['title']}, URL: {vacancy['url']}")

            store_vacancies_to_json(vacancies, 'vacancies.json')

            store_vacancies_to_sqlite(vacancies, 'vacancies.db')
        else:
            print("No vacancies found.")
    else:
        print("Failed to fetch the content.")
