import os
import requests
from bs4 import BeautifulSoup
import json

def fetch_page_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def save_content_to_file(content, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"Content saved to {filename}")

def load_content_from_file(filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    return None

def extract_quotes(content):
    soup = BeautifulSoup(content, 'html.parser')
    quotes_list = []

    for quote in soup.find_all('div', class_='quote'):
        text = quote.find('span', class_='text').get_text()
        author = quote.find('small', class_='author').get_text()
        quotes_list.append({
            'text': text,
            'author': author
        })

    return quotes_list

def get_next_page_url(content):
    soup = BeautifulSoup(content, 'html.parser')
    next_page_tag = soup.select_one('li.next a')
    if next_page_tag:
        return next_page_tag['href']
    return None

def save_quotes_to_json(quotes, filename):
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(quotes, json_file, ensure_ascii=False, indent=4)
    print(f"Quotes saved to {filename}")

if __name__ == "__main__":
    main_page_file = 'quotes_main_page.html'
    second_page_file = 'quotes_second_page.html'

    main_page_url = 'https://quotes.toscrape.com/'

    main_page_content = load_content_from_file(main_page_file)
    if not main_page_content:
        main_page_content = fetch_page_content(main_page_url)
        if main_page_content:
            save_content_to_file(main_page_content, main_page_file)

    second_page_url = None
    if main_page_content:
        next_page_path = get_next_page_url(main_page_content)
        if next_page_path:
            second_page_url = f"https://quotes.toscrape.com{next_page_path}"

    second_page_content = None
    if second_page_url:
        second_page_content = load_content_from_file(second_page_file)
        if not second_page_content:
            second_page_content = fetch_page_content(second_page_url)
            if second_page_content:
                save_content_to_file(second_page_content, second_page_file)

    quotes_main_page = extract_quotes(main_page_content) if main_page_content else []
    quotes_second_page = extract_quotes(second_page_content) if second_page_content else []

    all_quotes = quotes_main_page + quotes_second_page

    save_quotes_to_json(all_quotes, 'quotes.json')

    for quote in all_quotes:
        print(f"Text: {quote['text']}")
        print(f"Author: {quote['author']}")
        print()
