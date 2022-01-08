import csv
import json
from typing import List

import lxml.html
import requests
from bs4 import BeautifulSoup

URL = 'https://race.netkeiba.com/race/result.html?race_id=202106050811&rf=race_list'

# response = requests.get(URL)
# response.encoding = 'EUC-JP'
# print(response.text)


# tree = lxml.html.parse('./text.html')
# html = tree.getroot()
# html = lxml.html.fromstring(response.text)

# h1 = html.cssselect('h1')[0]
# print(h1.tag)
# print(h1.attrib)
# print(h1.get('title'))
# print(h1.text_content())

def bs(url: str):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    horse_name_list = soup.find_all('span', class_='Horse_Name')
    for horse_name in horse_name_list:
        h = horse_name.select('span > a')[0]
        print(h.get('title'), h.get('href'))
        print(horse_name.select('[]'))


def fetch_html_from_url(url: str) -> str:
    response = requests.get(url)
    response.encoding = 'EUC-JP'
    return response.text


def scrape(html: str, base_url: str) -> List[dict]:
    books = []
    html = lxml.html.fromstring(html)
    html.make_links_absolute(base_url)

    l = html.cssselect(
        '#All_Result_Table > tbody > tr:nth-child(1)')
    l = html.cssselect('a[href^="https://db.netkeiba.com/horse"]')
    l = html.cssselect('.Horse_Name')
    print(l)
    print(type(l), len(l))
    for a in l:
        print(a.attrib)
        url = a.cssselect('a[href^="https://"]')
        url = a.get('href')
        if url:
            print(url)
        else:
            print(url, 'ahh')

    # for a in html.cssselect(
    #         '#All_Result_Table > tbody > tr:nth-child(1) > td:nth-child(4)'):
    #     url = a.get('href')
    # print(url)
# All_Result_Table > tbody > tr:nth-child(1) > td:nth-child(4)
# All_Result_Table > tbody > tr:nth-child(1) > td:nth-child(4) > span


def save():
    pass


def main():
    bs(URL)
    # html = fetch_html_from_url(url=URL)
    # horses = scrape(html=html, base_url=URL)


if __name__ == '__main__':
    main()
