import urllib

import chardet
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag

URL = 'https://race.netkeiba.com/race/result.html?race_id=202106050811&rf=race_list'


def check_character_code() -> None:
    rawdata = urllib.request.urlopen(URL).read()
    ret = chardet.detect(rawdata)
    print(ret)


class ResultRecord(object):
    def __init__(self, tag: Tag) -> None:
        assert isinstance(tag, Tag), 'Invalid argument'
        self.rank = int(tag.select_one('.Rank').get_text(strip=True))
        self.waku = int(tag.select('.Num')[0].get_text(strip=True))
        self.txt_c = int(tag.select('.Num')[1].get_text(strip=True))
        self.odds_people = int(tag.select('.Odds')[0].get_text(strip=True))
        self.odds = float(tag.select('.Odds')[1].get_text(strip=True))
        print(self.__dict__)


def main():
    response = requests.get(URL)

    soup = BeautifulSoup(response.content, 'html.parser')
    header = soup.select_one('.Header')
    header_text = header.get_text(strip=True)
    print(header_text)

    horse_info_list = [horse_info for horse_info in soup.select('.HorseList')]
    print(f'Number of horses: {len(horse_info_list)}')
    for horse_index, horse_info in enumerate(horse_info_list):
        print(horse_index)
        result_record = ResultRecord(horse_info)


if __name__ == '__main__':
    check_character_code()
    main()
