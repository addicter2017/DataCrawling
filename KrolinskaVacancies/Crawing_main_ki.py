import requests
from requests.exceptions import RequestException
import re
import pymongo
import json
from bs4 import BeautifulSoup
from config import *
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]


def get_one_page(url,page):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
    }
    data = {
        'view_name': 'vacancies',
        'view_display_id': 'block_1',
        'view_args': '',
        'view_path': '/node/594',
        'view_base_path': 'vacancies',
        'view_dom_id': '641ff3aa3f53e304e007e7d2954ec229087aefc5c2153fbde3531635bae0cf36',
        'pager_element': 0,
        'dep': 'All',
        'type': 'All',
        'page': page,
        '_drupal_ajax': 1,
        'ajax_page_state[theme]': 'kise',
        'ajax_page_state[theme_token]': '',
        'ajax_page_state[libraries]': 'berzelius_core/berzelius-clientside-validation,chosen/drupal.chosen,chosen_lib/chosen.css,clientside_validation_jquery/cv.jquery.ckeditor,clientside_validation_jquery/cv.jquery.ife,clientside_validation_jquery/cv.jquery.validate,core/html5shiv,eu_cookie_compliance/eu_cookie_compliance,ki_group/toolbar,kise/kise_global,open_readspeaker/basic,open_readspeaker/post_mode,pdb/vue-search-block/footer,qbank_dam/qbank_resize,system/base,theorell/fonts,theorell/global,theorell/sanitize,theorell/slideshow,views/views.ajax,views/views.module'
    }
    try:
        response = requests.post(url,data,headers = headers)
        print(response.status_code)
        if response.status_code == 200:
            return response.text
        return None

    except RequestException:
        return None

def parse_one_page(html):
    j = json.loads(html)
    soup = BeautifulSoup(j[2]['data'], 'lxml')
    results = []
    listlenth = len(soup.find_all(target= '_blank'))
    for i in range(listlenth):
        results.append((soup.find_all(target = '_blank')[i]['href'],
                        soup.find_all(target = '_blank')[i].string,
                        soup.find_all('time')[i].string))
    return results

def main():
    url = 'https://ki.se/en/views/ajax?_wrapper_format=drupal_ajax'
    for i in range(3):
        html = get_one_page(url,i)
        results = parse_one_page(html)
        for result in results:
            result_dict = {
                'title':result[1],
                'address time':'',
                'link': result[0],
                'application deadline':result[2]
            }

            save_to_mongo(result_dict)

def save_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print('存储到数据库成功',result['title'])
        return True
    return False

if __name__ == '__main__':
    main()
