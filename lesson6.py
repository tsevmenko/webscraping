import requests
from bs4 import BeautifulSoup
import json

def fetch_sport_page():
    url = "https://www.bbc.com/sport"
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
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

def store_news_items_to_json(news_items, filename):
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(news_items, json_file, ensure_ascii=False, indent=4)
    print(f"News items stored in {filename}")

def parse_document(content):
    soup = BeautifulSoup(content, 'html.parser')
    news_items = []

    posts = soup.find_all('div', {'data-testid': 'promo'}, limit=5)

    for idx, post in enumerate(posts, start=1):
        ul_tag = post.find('ul', {'role': 'list'})
        topics = []
        link = None

        if ul_tag:
            li_tags = ul_tag.find_all('li', {'role': 'listitem'}, recursive=False)
            for li in li_tags:
                topic_tag = li.find('span', class_='ssrcss-1if1g9v-MetadataText')
                link_tag = li.find('a', href=True)
                if topic_tag and link_tag:
                    topics.append(topic_tag.get_text())
                    link = f"https://www.bbc.com{link_tag['href']}"

        if not link:
            link_tag = post.find('a', href=True)
            link = f"https://www.bbc.com{link_tag['href']}" if link_tag else "No link found"

        news_items.append({
            'Link': link,
            'Topics': topics
        })

    return news_items

if __name__ == "__main__":
    content = fetch_sport_page()
    if content:
        save_content_to_file(content, 'bbc_sport_content.html')

    content = load_content_from_file('bbc_sport_content.html')
    news_items = parse_document(content)
    store_news_items_to_json(news_items, 'bbc_sport_news_items.json')

    for item in news_items:
        print(f"Link: {item['Link']}")
        print(f"Topics: {item['Topics']}")
        print()
