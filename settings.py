import os

DB_NAME = 'scrapedb'
USER_NAME = 'scraper'
SCRAPE_SCHEMA_NAME = 'scrape'

HTML_TABLE_NAME = 'race_result_htmls'

RACE_DB_BASE_URL = 'https://db.netkeiba.com/'
RACE_RESULT_BASE_URL = 'https://race.netkeiba.com/race/result.html'

START_DATE = '2021'
END_DATE = '2022'

HTML_DIRECTORY = os.getenv('PGHTML')
