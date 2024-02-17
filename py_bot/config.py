import os
from dotenv import load_dotenv
from typing import Final
import logging

load_dotenv()

TOKEN: Final = os.getenv('TOKEN')
BOT_NAME: Final = os.getenv('BOT_NAME')
SERVER_URL: Final = os.getenv('SERVER_URL')
LOG_LEVEL: Final = os.getenv('LOG_LEVEL') or 'INFO'

logging.basicConfig(level=LOG_LEVEL.upper())

if not all([TOKEN, BOT_NAME, SERVER_URL]):
    raise SystemExit('Err: Missing environment variables')
