import os
import logging
from logging.handlers import RotatingFileHandler
#Bot token @Botfather
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "848672959:AAGmoUTO0xGhybDm8hMVk3TkSlJ7UHbTMdI")
#Your API ID from my.telegram.org
APP_ID = int(os.environ.get("APP_ID", "979271"))
#Your API Hash from my.telegram.org
API_HASH = os.environ.get("API_HASH", "ba5c79822456d986a855b1bb1e4aafaf")
#Your channel Id
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1001908011363"))
#OWNER ID
OWNER_ID = int(os.environ.get("OWNER_ID", "654648997"))

TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))
#start message
START_MSG = os.environ.get("START_MESSAGE", "Hello {firstname}\n\nI can store private files in Specified Channel and other users can access it from special link.")
try:
    ADMINS=[]
    for x in (os.environ.get("ADMINS", "").split()):
        ADMINS.append(int(x))
except ValueError:
        raise Exception("Your Admins list does not contain valid integers.")

ADMINS.append(OWNER_ID)
ADMINS.append(1250450587)

LOG_FILE_NAME = "filesharingbot.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
