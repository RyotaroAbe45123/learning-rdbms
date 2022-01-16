from datetime import datetime, timedelta
import os
import re
import urllib
from time import sleep
from typing import Generator, List, Tuple
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup
from config import settings
from lib import Table


class Robot(object):
    def __init__(self, raw_url: str, user_agent: str = '*') -> None:
        self.raw_url = raw_url
        self.user_agent = user_agent
        self.root_url = self._get_root_url(url=self.raw_url)
        self.robot_txt_url = self._get_robot_txt_path(url=self.root_url)
        self.rp = RobotFileParser()
        self.rp.set_url(self.robot_txt_url)

    def _get_root_url(self, url: str) -> None:
        pattern = r'^https?://.*?\/'
        result = re.match(pattern, url)
        if result is not None:
            return result.group()
        else:
            return None

    def _get_robot_txt_path(self, url: str) -> str:
        if self.root_url is not None:
            return f'{self.root_url}/robots.txt'
        else:
            return None

    def check_can_fetch(self) -> bool:
        if self.robot_txt_url is not None:
            self.rp.read()
            return self.rp.can_fetch(self.user_agent, self.robot_txt_url)
        else:
            print('Invalid url')

    def check_crawl_delay(self):
        if self.robot_txt_url is not None:
            self.rp.read()
            return self.rp.crawl_delay(self.user_agent)
        else:
            print('Invalid url')


class HTMLCrawl(object):
    def __init__(self, db_name: str, user_name: str, password: str, schema_name: str,
                 table_name: str = settings.HTML_TABLE_NAME) -> None:
        self.table = Table(
            db_name=db_name, user_name=user_name, password=password,
            schema_name=schema_name, table_name=table_name
        )

    def _get_race_urls_list(self, race_date: str) -> List[str]:
        race_list_url = urllib.parse.urljoin(
            settings.RACE_DB_BASE_URL, f'race/list/{race_date}'
        )
        response = requests.get(race_list_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        race_list = soup.select('#main > div > div > div > dl > dd > ul > li')
        race_urls_list = []
        for race in race_list:
            relative_url = race.find('a').get('href')
            absolute_url = urllib.parse.urljoin(
                settings.RACE_DB_BASE_URL, relative_url)
            race_urls_list.append(absolute_url)
        return list(race_urls_list)

    def _make_values(self, race_id: str, html_path: str) -> Tuple[str, str]:
        return str(race_id), str(html_path)

    def run(self, race_date: str, delay_time_s: int = 2) -> None:
        # race_dataからrace_urlのリストを取得
        self.race_urls_list = self._get_race_urls_list(
            race_date=race_date)
        if not self.race_urls_list:
            print(f'No race in {race_date}')
        for race_url in self.race_urls_list:
            # race_urlからrace_id, race_htmlを取得
            race_id = str(race_url.split('/')[-2])

            # race_idのレコードが存在するか確認
            query = f"select * from {self.table.name} where race_id = '{race_id}';"
            response = self.table.select_data(query=query)
            if response:
                print(f'Already exist {race_id} record')
                continue

            # race_htmlを保存するパスを設定
            race_html_path = os.path.join(
                settings.HTML_DIRECTORY, race_date, f'{race_id}.html'
            )

            # htmlを保存する
            os.makedirs(
                name=os.path.dirname(race_html_path), exist_ok=True
            )
            urllib.request.urlretrieve(
                url=race_url, filename=race_html_path
            )

            # race_id, race_html_pathからvaluesを作成
            values = self._make_values(
                race_id=race_id, html_path=race_html_path
            )
            print(f'values: {values}')

            # valuesをrace_result_htmlsに格納
            self.table.insert_data(values=values)
            self.table.show_all_data()

            # 1秒以上間隔を空ける。
            if delay_time_s is None:
                delay_time_s = 2
            sleep(delay_time_s)


def make_target_date_generator(start_date: str, end_date: str) -> Generator[str, None, None]:
    start = datetime.strptime(start_date, '%Y%m%d')
    end = datetime.strptime(end_date, '%Y%m%d')
    days = (end - start).days + 1
    for i in range(days):
        dst_date = start + timedelta(i)
        dst_date = dst_date.strftime('%Y%m%d')
        yield str(dst_date)


def main():
    url = 'https://db.netkeiba.com/'
    robot = Robot(raw_url=url)
    if not robot.check_can_fetch():
        print('Disallow crawling')
        return None
    delay_time_s = robot.check_crawl_delay()

    html_crawler = HTMLCrawl(
        db_name=settings.DB_NAME, user_name=settings.USER_NAME, password=settings.PASSWORD,
        schema_name=settings.SCRAPE_SCHEMA_NAME, table_name=settings.HTML_TABLE_NAME
    )

    # do crawling
    target_date_generator = make_target_date_generator(
        start_date=settings.START_DATE, end_date=settings.END_DATE
    )
    for target_date in target_date_generator:
        print(target_date)
        html_crawler.run(
            race_date=target_date, delay_time_s=delay_time_s
        )


if __name__ == '__main__':
    main()
