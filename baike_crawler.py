import requests
from bs4 import BeautifulSoup

header = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G955U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36'
}


def parse_baike(word):
    # print("-->",word)

    response = requests.get(f'https://baike.baidu.com/item/{word}', headers=header)

    bs = BeautifulSoup(response.text, 'html.parser')

    sub_title = []
    # 解析 lemma
    lemma = bs.find('li', {'class': 'extra-list-item extra-lemma-desc'})
    if lemma is not None:
        sub_title.append(lemma.text)

    # 解析 描述
    meta = bs.find('meta', {'name': 'description'})
    description = meta['content'] if meta is not None and meta['content'] is not None else ''

    # 解析配料应用
    basic_info_list = bs.find_all('li', {'class': 'basicInfo-hide'})
    for basic_info in basic_info_list:
        title = basic_info.find('div', {'class': 'info-title'}).text.strip()
        content = basic_info.find('div', {'class': 'info-content'}).text.strip()

        if title in ('应用', '属性'):
            sub_title.append(content)

    return '，'.join(sub_title), description
