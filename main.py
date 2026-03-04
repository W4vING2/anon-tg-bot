import asyncio
import logging

from aiogram.types import BotCommand
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from config import bot, dp, WEBHOOK_HOST, WEBHOOK_URL, WEBHOOK_PATH, PORT
from handlers import commands_router, relay_router

dp.include_router(commands_router)
dp.include_router(relay_router)


async def set_commands():
    await bot.set_my_commands([
        BotCommand(command="start", description="Главное меню"),
        BotCommand(command="invite", description="Создать приглашение"),
        BotCommand(command="stop", description="Завершить чат"),
    ])


async def on_startup(app):
    await set_commands()
    await bot.set_webhook(WEBHOOK_URL)
    print(f"Webhook установлен: {WEBHOOK_URL}")


async def on_shutdown(app):
    await bot.delete_webhook()


async def run_polling():
    logging.basicConfig(level=logging.INFO)
    print("Запуск в режиме polling (локально)...")
    await set_commands()
    await dp.start_polling(bot)


def main():
    logging.basicConfig(level=logging.INFO)

    if not WEBHOOK_HOST:
        asyncio.run(run_polling())
        return

    app = web.Application()
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)

    web.run_app(app, host="0.0.0.0", port=PORT)


if __name__ == "__main__":
    main()
