import os
from pathlib import Path

from dotenv import load_dotenv

env_file_path = os.path.join(Path(__file__).parent.parent, '.env')
load_dotenv(env_file_path)

DB_NAME = os.getenv('DB_NAME')
USER_NAME = os.getenv('USER_NAME')
PASSWORD = os.getenv('PASSWORD')
SCRAPE_SCHEMA_NAME = os.getenv('SCHEMA_NAME')

HTML_DIRECTORY = os.getenv('PGHTML')

HTML_TABLE_NAME = 'race_result_htmls'

RACE_DB_BASE_URL = 'https://db.netkeiba.com/'
# RACE_RESULT_BASE_URL = 'https://race.netkeiba.com/race/result.html'

START_DATE = '20211220'
END_DATE = '20211226'
