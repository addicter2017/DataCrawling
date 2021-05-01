# -*- coding: utf-8 -*-
# @Time    : 2020/8/28 14:02
# @Author  : Can Zhang
# @FileName: crawing_main_lulea.py
# @Software: PyCharm
# -*- coding: utf-8 -*-
# @Time    : 2020/8/24 1:43
# @Author  : Can Zhang
# @FileName: Request+正则爬取Chalmers.py
# @Software: PyCharm
import requests
from requests.exceptions import RequestException
import re
import pymongo
from config import *
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]


def get_one_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
    }
    try:
        response = requests.get(url,headers = headers)
        print(response.status_code)
        if response.status_code == 200:
            return response.text
        return None

    except RequestException:
        return None

def parse_one_page(html):
    pattern = re.compile(r'class="jobitem".*?<a.*?href="(.*?)".*?title="(.*?)">(.*?)</a>.*?</span>(.*?)</td>',re.S)
    return re.findall(pattern,html)

def main():
    url = 'https://web103.reachmee.com/ext/I009/613/main?site=7&validator=696d86b542bf9f7d3a3da97c96c9eb28&lang=UK&ref=https%3a%2f%2flnu.se%2fen%2fmeet-linnaeus-university%2fwork-at-the-university%2finterviews-with-members-of-staff%2f&ihelper=https://lnu.se/en/meet-linnaeus-university/work-at-the-university/'
    html = get_one_page(url)

    results = parse_one_page(html)
    for result in results:
        result_dict = {
            'UNIname': 'LNU',
            'title':result[2],
            'address_time':result[1],
            'link': result[0],
            'application_deadline':result[3].lstrip()
        }
        #print(result_dict)
        save_to_mongo(result_dict)

def save_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print('存储到数据库成功',result['title'])
        return True
    return False

# if __name__ == '__main__':
main()

