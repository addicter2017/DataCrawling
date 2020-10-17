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
    pattern = re.compile(r'class="jobitem".*?<a.*?href="(.*?)".*?title="(.*?)">(.*?)</a>.*?none">(.*?)</span>',re.S)
    return re.findall(pattern,html)

def main():
    url_1 = 'https://web103.reachmee.com/ext/I007/927/main?site=8&validator=d3e6a58db9058c5eab7ea3e324f063f6&lang=UK&ref=https%3a%2f%2fwww.su.se%2fenglish%2fabout%2fworking-at-su&ihelper=https://www.su.se/english/about/working-at-su/jobs'
    url_2 = 'https://web103.reachmee.com/ext/I007/927/main?site=13&validator=da57c1f2e2ddea2946680e7e5adb241d&lang=UK&ref=&ihelper=https://www.su.se/english/about/working-at-su/phd'
    url_list = [url_1,url_2]
    for url in url_list:
        html = get_one_page(url)
        results = parse_one_page(html)
        for result in results:
            result_dict = {
                'title':result[2],
                'address time':result[1],
                'link': result[0],
                'application deadline':result[3]
            }
            save_to_mongo(result_dict)
def save_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print('存储到数据库成功',result['title'])
        return True
    return False

if __name__ == '__main__':
    main()
