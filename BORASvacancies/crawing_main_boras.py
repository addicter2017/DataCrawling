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
    url = 'https://web103.reachmee.com/ext/I009/946/main?site=11&validator=b60ba67aae6879c89456ea3cb3a48b5e&lang=UK&ref=https%3a%2f%2fwww.hb.se%2fen%2fabout-ub%2f&ihelper=http://www.hb.se/en/About-UB/Work-at-UB/Job-vacancies/'
    html = get_one_page(url)

    results = parse_one_page(html)
    for result in results:
        result_dict = {
            'title':result[2],
            'address time':result[1],
            'link': result[0],
            'application deadline':result[3].strip()
        }
        #print(result_dict)
        save_to_mongo(result_dict)

def save_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print('存储到数据库成功',result['title'])
        return True
    return False

if __name__ == '__main__':
    main()

