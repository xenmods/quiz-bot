from pyrogram import Client
from httpx import AsyncClient
import logging
import uvloop
from Bot.config import Config

uvloop.install()
bot = Client("quizbot", Config.API_ID, Config.API_HASH, bot_token=Config.BOT_TOKEN)
session = AsyncClient(timeout=30)
ACTIVE_QUIZZES = {}

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)
