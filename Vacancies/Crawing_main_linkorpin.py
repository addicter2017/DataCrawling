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
    pattern = re.compile(r'class="jobitem".*?<a href="(.*?)".*?title="(.*?)">(.*?)</a>.*?</span>(.*?)</td>',re.S)
    return re.findall(pattern,html)

def main():
    url = 'https://web103.reachmee.com/ext/I011/853/main?site=7&validator=d7a66c13be778ef950c393a904293789&lang=UK&ref=https%3a%2f%2fliu.se%2fen%2fwork-at-liu&ihelper=https://liu.se/en/work-at-liu/vacancies'

    html = get_one_page(url)

    results = parse_one_page(html)
    for result in results:
        result_dict = {
            'UNIname': 'LINKORPIN',
            'title':result[2],
            'address_time':result[1],
            'link': result[0],
            'application_deadline':result[3].lstrip()
        }

        save_to_mongo(result_dict)

def save_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print('存储到数据库成功',result['title'])
        return True
    return False

# if __name__ == '__main__':
main()
