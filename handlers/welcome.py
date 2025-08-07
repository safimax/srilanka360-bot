from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from states.bot_states import BotStates
from utils.text_utils import get_text, get_keyboard

router = Router()

@router.callback_query(F.data == "готов_к_эксклюзивному_отдыху")
async def handle_ready_exclusive(callback: CallbackQuery, state: FSMContext):
    """UTM/внешние пользователи: переход к вопросам"""
    current_state = await state.get_state()
    data = await state.get_data()
    
    if current_state == BotStates.WELCOME_UTM and data.get("villa_id"):
        villa_id = data["villa_id"]
        text = get_text("screens.villa_utm_detected.message").format(villa_id=villa_id)
        keyboard = get_keyboard(["🏠 Перейти к датам и деталям"])
        
        await callback.message.edit_text(text, reply_markup=keyboard)
        await state.set_state(BotStates.VILLA_UTM_DETECTED)
    else:
        await show_questions_start(callback, state)
    
    await callback.answer()

@router.callback_query(F.data == "подобрать_виллу_по_параметрам")
async def handle_select_villa(callback: CallbackQuery, state: FSMContext):
    """Канальные пользователи: сразу к развилке"""
    from handlers.villa import show_villa_fork
    await show_villa_fork(callback.message, state)
    await callback.answer()

@router.callback_query(F.data == "перейти_к_датам_и_деталям")
async def handle_villa_utm_confirmed(callback: CallbackQuery, state: FSMContext):
    """UTM пользователь подтвердил интерес к вилле"""
    from handlers.group import show_group_type
    await show_group_type(callback.message, state)
    await callback.answer()

async def show_questions_start(callback: CallbackQuery, state: FSMContext):
    """Показ экрана вопросов для внешних пользователей"""
    text = get_text("screens.questions_start.message")
    keyboard = get_keyboard(["💎 Подобрать виллу по параметрам"])
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await state.set_state(BotStates.QUESTIONS_START)