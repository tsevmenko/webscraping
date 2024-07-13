import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

def fetch_job_listings():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    driver.get('https://jobs.marksandspencer.com/job-search')

    time.sleep(5)

    jobs = []

    def extract_jobs_from_page():
        job_elements = driver.find_elements(By.CSS_SELECTOR, 'li.ais-Hits-item')
        for job_element in job_elements:
            try:
                title_element = job_element.find_element(By.CSS_SELECTOR, 'h3')
                title = title_element.text

                url_element = job_element.find_element(By.CSS_SELECTOR, 'a.c-btn.c-btn--primary')
                url = url_element.get_attribute('href')

                jobs.append({
                    'title': title,
                    'url': url
                })
            except NoSuchElementException as e:
                print(f"Error: {e} - Skipping this job listing.")
                continue

    extract_jobs_from_page()

    try:
        next_page_link = driver.find_element(By.CSS_SELECTOR, 'li.ais-Pagination-item--page a[aria-label="Page 2"]')
        next_page_link.click()

        time.sleep(5)

        extract_jobs_from_page()
    except NoSuchElementException as e:
        print(f"Error: {e} - Could not find the second page link.")

    driver.quit()

    return jobs

def save_jobs_to_json(jobs, filename):
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(jobs, json_file, ensure_ascii=False, indent=4)
    print(f"Jobs saved to {filename}")

if __name__ == "__main__":
    jobs = fetch_job_listings()
    save_jobs_to_json(jobs, 'jobs.json')

    for job in jobs:
        print(f"Title: {job['title']}")
        print(f"URL: {job['url']}")
        print()
