import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_HOST = os.getenv("RENDER_EXTERNAL_URL", "")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
PORT = int(os.getenv("PORT", 8000))

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

pending_invites: dict[str, int] = {}
active_chats: dict[int, int] = {}
