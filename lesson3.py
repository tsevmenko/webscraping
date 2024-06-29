import re
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

def read_html_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def parse_dates():
    date_pattern = re.compile(
        r'(\b\d{1,2}[/-]\d{1,2}[/-]\d{4}\b)'        # MM/DD/YYYY or MM-DD-YYYY
        r'|(\b\d{4}[./]\d{1,2}[./]\d{1,2}\b)'       # YYYY.MM.DD or YYYY/MM/DD
        r'|(\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w* \d{1,2}, \d{4}\b)',  # month names
        re.IGNORECASE
    )

    # Find all dates in the text
    dates = date_pattern.findall(text)

    # Flatten the list of tuples
    dates = [date for group in dates for date in group if date]

    # Print the found dates
    for date in dates:
        print(date)

def parse_phone_numbers():
    phone_pattern = re.compile(
        r'(\(\d{3}\)\s?\d{3}-\d{4})'            # (123) 456-7890
        r'|(\+\d{1,2}-\d{3}-\d{3}-\d{4})'       # +1-800-555-1234
        r'|(\d{3}[.-]\d{3}[.-]\d{4})'           # 800.555.1234, 800-555-1234, 123.456.7890
        r'|(\+\d{1,2}\s\d{1,4}\s\d{3,4}\s\d{3,4})' # +44 20 7946 0958, +91 98765 43210
    )

    phone_numbers = phone_pattern.findall(text)

    for phone in phone_numbers:
        print(phone)

# i've tried
def parse_html_file():
    file_path = 'example.html'
    html_content = read_html_file(file_path)

    if html_content:
        print("HTML content loaded successfully.")
        soup = BeautifulSoup(html_content, 'html.parser')

        # Try to find the element with ID 'text-input-what'
        search_field = soup.find_all("form")

        if search_field:
            print("Search field found:", search_field)
        else:
            print("Search field with id 'text-input-what' not found.")
            # Find elements close to the target ID
            nearby_elements = soup.find_all(attrs={'id': re.compile(r'.*text-input.*', re.IGNORECASE)})
            if nearby_elements:
                print("Nearby elements with similar IDs:")
                for elem in nearby_elements:
                    print(elem)
            else:
                print("No elements with similar IDs found.")

if __name__ == '__main__':
#     parse_dates()
#     parse_phone_numbers()
#     parse_html_file() - this function doesn't work because of JS :)
#     but here is XPath
#     search input - //*[@id="text-input-what"]
#     place input - //*[@id="text-input-where"]
#     input - //*[@id="jobsearch"]//button
