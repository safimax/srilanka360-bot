import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Конфигурация
BOT_TOKEN = os.getenv("BOT_TOKEN", "7030170141:AAF2kUW25wr8CfSLESKMwPQh8KCX4Jb_R-k")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = None  # Будет установлен автоматически

async def on_startup(bot: Bot):
    """Инициализация при запуске"""
    # Webhook URL будет установлен Cloud Run автоматически
    logger.info("Bot startup complete")

async def create_app():
    """Создание приложения"""
    # Инициализация бота
    bot = Bot(token=BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    
    # Подключение обработчиков
    from handlers.start import router as start_router
    from handlers.welcome import router as welcome_router
    from handlers.villa import router as villa_router
    from handlers.group import router as group_router
    from handlers.errors import router as errors_router
    
    dp.include_routers(
        start_router,
        welcome_router,
        villa_router,
        group_router,
        errors_router
    )
    
    # Запуск инициализации
    await on_startup(bot)
    
    # Создание веб-приложения
    app = web.Application()
    
    # Добавляем главную страницу для проверки
    async def index(request):
        return web.Response(text="Sri Lanka 360 Bot is running! Bot ready for Telegram webhooks.")
    
    app.router.add_get('/', index)
    
    # Настройка webhook
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)
    
    return app

def main():
    """Запуск приложения"""
    port = int(os.environ.get('PORT', 8080))
    
    # Создаем и запускаем приложение
    app = asyncio.new_event_loop().run_until_complete(create_app())
    web.run_app(app, host='0.0.0.0', port=port)

if __name__ == '__main__':
    main()