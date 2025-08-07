from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from states.bot_states import BotStates
from utils.text_utils import get_text, get_keyboard

router = Router()

@router.message(Command("start"))
async def handle_start(message: Message, command: CommandObject, state: FSMContext):
    """Обработка команды /start с определением сценария входа"""
    start_param = command.args
    user_id = message.from_user.id
    
    # Определяем сценарий входа
    if start_param and "VILLA_" in start_param:
        # UTM с виллой
        villa_id = extract_villa_id(start_param)
        await state.update_data(
            entry_point=start_param,
            villa_id=villa_id
        )
        await show_welcome_utm(message, state, villa_id)
        
    elif start_param == "channel_general":
        # Из шапки канала
        await state.update_data(entry_point="channel_general")
        await show_welcome_channel(message, state)
        
    else:
        # Внешний / прямой вход
        entry_point = start_param or "direct"
        await state.update_data(entry_point=entry_point)
        await show_welcome_external(message, state)

def extract_villa_id(start_param: str) -> str:
    """Извлечение villa_id из UTM параметра"""
    if "VILLA_" in start_param:
        return start_param.split("_UTM")[0]
    return None

async def show_welcome_utm(message: Message, state: FSMContext, villa_id: str):
    """UTM вход - показать Привет мир + вилла определена"""
    text = get_text("screens.welcome_utm.message")
    keyboard = get_keyboard(["🚀 Готов к эксклюзивному отдыху"])
    
    await message.answer(text, reply_markup=keyboard)
    await state.set_state(BotStates.WELCOME_UTM)

async def show_welcome_channel(message: Message, state: FSMContext):
    """Канал вход - сразу к 5 вопросам"""
    text = get_text("screens.welcome_channel.message") 
    keyboard = get_keyboard(["💎 Подобрать виллу по параметрам"])
    
    await message.answer(text, reply_markup=keyboard)
    await state.set_state(BotStates.WELCOME_CHANNEL)

async def show_welcome_external(message: Message, state: FSMContext):
    """Внешний вход - Привет мир + переход к вопросам"""
    text = get_text("screens.welcome_external.message")
    keyboard = get_keyboard(["🚀 Готов к эксклюзивному отдыху"])
    
    await message.answer(text, reply_markup=keyboard)
    await state.set_state(BotStates.WELCOME_EXTERNAL)