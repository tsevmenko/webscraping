import requests
import re

payload = {
     "action": "facetwp_refresh",
     "data": {
         "facets": {
             "recherche": [],
             "ou": [],
             "type_de_contrat": [],
             "fonction": [],
             "load_more": [
                 2
             ]
         },
         "frozen_facets": {
             "ou": "hard"
         },
         "http_params": {
             "get": [],
             "uri": "emplois",
             "url_vars": []
         },
         "template": "wp",
         "extras": {
             "counts": True,
             "sort": "default"
         },
         "soft_refresh": 1,
         "is_bfcache": 1,
         "first_load": 0,
         "paged": 1
     }
 }

def get_data_for_page(url, page):
    payload["data"]["paged"] = page
    response = requests.post(url, json=payload)

    content = response.json()["template"]
    if response.status_code == 200:
        job_titles = []
        return re.findall(r'\"jobCard_title\">(.*?)<\/h3>', content)
    else:
        print("Error:", response.status_code)
        return []

if __name__ == '__main__':
    res = get_data_for_page("https://www.lejobadequat.com/emplois", 3)
    print(res)
