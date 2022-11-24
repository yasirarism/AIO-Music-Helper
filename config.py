import os
import logging
from os import getenv
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
LOGGER = logging.getLogger(__name__)

if not os.environ.get("ENV"):
    load_dotenv('.env', override=True)

class Config(object):
#--------------------

# MAIN BOT VARIABLES

#--------------------
    try:
        TG_BOT_TOKEN = getenv("TG_BOT_TOKEN")
        APP_ID = int(getenv("APP_ID", 123))
        API_HASH = getenv("API_HASH")
    except:
        LOGGER.warning("Essential TG Configs are missing")
        exit(1)

    try:
        AUTH_CHAT = set(int(x) for x in getenv("AUTH_CHAT").split())
    except:
        AUTH_CHAT = ""
    try:
        ADMINS = set(int(x) for x in getenv("ADMINS").split())
    except:
        LOGGER.warning("NO ADMIN USER IDS FOUND")
        exit(1)
    
    IS_BOT_PUBLIC = getenv("IS_BOT_PUBLIC", True)

    try:
        AUTH_USERS = set(int(x) for x in getenv("AUTH_USERS").split())
    except:
        AUTH_USERS = ""

    WORK_DIR = getenv("WORK_DIR", "./bot/")
    DOWNLOADS_FOLDER = getenv("DOWNLOADS_FOLDER", "DOWNLOADS")
    DOWNLOAD_BASE_DIR = WORK_DIR + DOWNLOADS_FOLDER
    
    BOT_USERNAME = getenv("BOT_USERNAME", "")
    if not BOT_USERNAME:
        LOGGER.warning("NO BOT USERNAME FOUND")
        exit(1)
    
    DATABASE_URL = getenv("DATABASE_URL")
    if not DATABASE_URL:
        LOGGER.warning("NO DATABASE URL FOUND")
        exit(1)

    BOT_LANGUAGE = getenv("BOT_LANGUAGE", "en")
    MENTION_USERS = getenv("MENTION_USERS", False)
    ANIT_SPAM_MODE = getenv("ANIT_SPAM_MODE", False)
#--------------------

# TIDAL VARIABLES

#--------------------
    TIDAL_EMAIL = getenv("TIDAL_EMAIL", "")
    TIDAL_PASSWORD = getenv("TIDAL_PASSWORD", "")
    TIDAL_TRACK_FORMAT = getenv("TIDAL_TRACK_FORMAT", "{TrackTitle} - {ArtistName}")
#--------------------

# KKBOX VARIABLES

#--------------------
    KKBOX_KEY = getenv("KKBOX_KEY", "")
    KKBOX_EMAIL = getenv("KKBOX_EMAIL", "")
    KKBOX_PASSWORD = getenv("KKBOX_PASSWORD", "")
#--------------------

# QOBUZ VARIABLES

#--------------------
    QOBUZ_EMAIL = getenv("QOBUZ_EMAIL", "")
    QOBUZ_PASSWORD = getenv("QOBUZ_PASSWORD", "")
    QOBUZ_TRACK_FORMAT = getenv("QOBUZ_TRACK_FORMAT", "{tracknumber}. {tracktitle}")


    if BOT_USERNAME.startswith("@"):
        BOT_USERNAME = BOT_USERNAME[1:]
