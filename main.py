import urllib

import chardet
import psycopg2
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag

import settings

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


def insert_data_into_db(db_name: str, user_name: str):
    conn = psycopg2.connect(f'dbname={db_name} user={user_name}')
    cursor = conn.cursor()
    # cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")
    cursor.execute('begin transaction;')
    cursor.execute("insert into race_result values (3, 'htest2');")
    cursor.execute("select * from race_result;")
    print(cursor.fetchall())
    cursor.execute('commit;')
    cursor.close()


def main():
    insert_data_into_db(
        db_name=settings.DB_NAME, user_name=settings.USER_NAME
    )


if __name__ == '__main__':
    check_character_code()
    main()
