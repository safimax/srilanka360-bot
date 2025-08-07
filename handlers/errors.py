from aiogram import Router
from aiogram.types import Message
from utils.text_utils import get_text

router = Router()

@router.message()
async def handle_unexpected_message(message: Message):
    """Обработка неожиданных сообщений"""
    error_text = get_text("messages.error_invalid_input")
    await message.answer(error_text)