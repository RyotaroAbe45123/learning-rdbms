import os
from typing import Generator
from urllib.parse import urljoin

import psycopg2
import requests
from bs4 import BeautifulSoup

import settings


class RaceResult(object):
    def __init__(self, race_url: str) -> None:
        response = requests.get(race_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.horse_info_list = soup.find('table').find_all('tr')[1:]
        self.race_id = int(race_url.split('/')[-2])

    def make_record_generator(self) -> Generator[dict, None, None]:
        for horse_info in self.horse_info_list:
            self.horse_id = int(horse_info.find(
                'a').get('href').split('/')[-2])
            td_list = horse_info.find_all('td')
            self.rank = int(td_list[0].get_text(strip=True))
            self.frame_order = int(td_list[1].get_text(strip=True))
            self.horse_order = int(td_list[2].get_text(strip=True))
            self.odds = float(td_list[12].get_text(strip=True))
            yield dict(
                race_id=self.race_id, horse_id=self.horse_id,
                rank=self.rank,
                frame_order=self.frame_order, horse_order=self.horse_order,
                odds=self.odds
            )


def make_race_list_generator(date: str) -> Generator[str, None, None]:
    race_list_url = urljoin(settings.RACE_DB_BASE_URL, f'race/list/{date}')
    response = requests.get(race_list_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    race_list = soup.select('#main > div > div > div > dl > dd > ul > li')
    for race in race_list:
        tmp_url = race.find('a').get('href')
        url = urljoin(settings.RACE_DB_BASE_URL, tmp_url)
        yield url


class ScrapeDB(object):
    def __init__(self, db_name: str, user_name: str,
                 schema_name: str = None) -> None:
        self.db_name = db_name
        self.user_name = user_name
        self.schema_name = schema_name

    def begin_connection(self) -> psycopg2.extensions.connection:
        if self.schema_name is not None:
            connect = psycopg2.connect(
                dbname=self.db_name,
                user=self.user_name,
                options=f'-c search_path={self.schema_name}'
            )
        else:
            connect = psycopg2.connect(
                dbname=self.db_name,
                user=self.user_name
            )
        return connect

    def insert_data_into_table(self, table_name: str, values: tuple):
        with self.begin_connection() as connect:
            with connect.cursor() as cursor:
                try:
                    query = f"insert into {table_name} values {values};"
                    cursor.execute(query)
                    cursor.execute('commit;')
                except psycopg2.errors.UniqueViolation as error:
                    print(error)
                except Exception as error:
                    print(error)
                    cursor.execute('rollback;')

    # def insert_data_into_table(self, table_name: str, values: tuple):
    #     self.begin_connect()
    #     cursor = self.connect.cursor()
    #     cursor.execute('begin transaction;')
    #     query = f"insert into {table_name} values {values};"
    #     try:
    #         cursor.execute(query)
    #     except BaseException as e:
    #         print(e)
    #         # cursor.execute('rollback;')
    #     # cursor.execute('update race_results set odds=10 where race_id=1;')
    #     # cursor.execute(f"select * from {table_name};")
    #     # print(cursor.fetchall())
    #     # cursor.execute('commit;')
    #     cursor.close()
    #     self.end_connect(self.connect)


class ScrapePipeline(object):
    pass


def main():
    target_date = '20211226'
    race_list_generator = make_race_list_generator(date=target_date)
    for race_index, race_url in enumerate(race_list_generator, start=1):
        race_record = RaceResult(race_url=race_url)
        race_record_generator = race_record.make_record_generator()
        break
    for record_dict in race_record_generator:
        # print(f'dict: {record_dict}')
        # dict -> tuple
        record_tuple = tuple(record_dict.values())
        # print(type(record_tuple))
        print(f'tuple: {record_tuple}')
        break
    scrapedb = ScrapeDB(
        db_name=settings.DB_NAME,
        user_name=settings.USER_NAME,
        schema_name=settings.SCHEMA_NAME)
    scrapedb.insert_data_into_table(
        table_name='race_results', values=record_tuple
    )
    return None


if __name__ == '__main__':
    main()
