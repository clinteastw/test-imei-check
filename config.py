import os

from dotenv import load_dotenv

load_dotenv()

ADMIN_IDS = (553128027, 123, 59, )
BOT_API_URL = os.environ.get("BOT_API_URL")
BOT_API_TOKEN = os.environ.get("BOT_API_TOKEN")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
IMEI_CHECK_API_URL = os.environ.get("IMEI_CHECK_API_URL")
IMEI_CHECK_SANDBOX_TOKEN = os.environ.get("IMEI_CHECK_SANDBOX_TOKEN")