from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from states.bot_states import BotStates
from utils.text_utils import get_text, get_keyboard

router = Router()

@router.callback_query(F.data == "есть_ссылканомер_виллы")
async def handle_have_link(callback: CallbackQuery, state: FSMContext):
    """Пользователь выбрал 'Есть ссылка/номер виллы'"""
    text = "Отлично! Пришлите ссылку на виллу или укажите её номер:"
    await callback.message.edit_text(text)
    await state.set_state(BotStates.VILLA_INPUT)
    await callback.answer()

@router.callback_query(F.data == "хочу_описать_мечту")
async def handle_want_dream(callback: CallbackQuery, state: FSMContext):
    """Пользователь выбрал 'Хочу описать мечту'"""
    text = get_text("screens.dream_form.message")
    await callback.message.edit_text(text)
    await state.set_state(BotStates.DREAM_FORM)
    await callback.answer()

@router.message(BotStates.VILLA_INPUT)
async def handle_villa_input_text(message: Message, state: FSMContext):
    """Обработка введенной ссылки/номера"""
    user_input = message.text.strip()
    await state.update_data(villa_input_raw=user_input)
    
    confirmation = f"Отлично! Передадим эксперту: \"{user_input}\""
    await message.answer(confirmation)
    
    from handlers.group import show_group_type
    await show_group_type(message, state)

@router.message(BotStates.DREAM_FORM)
async def handle_dream_form_text(message: Message, state: FSMContext):
    """Обработка описания мечты"""
    dream_text = message.text.strip()
    
    # Простое извлечение бюджета
    budget = extract_budget_from_text(dream_text)
    
    await state.update_data(
        dream_description=dream_text,
        budget_mentioned=budget or "not_specified"
    )
    
    await message.answer("Отлично! Учтем ваши пожелания.")
    
    from handlers.group import show_group_type
    await show_group_type(message, state)

def extract_budget_from_text(text: str) -> str:
    """Простое извлечение бюджета из текста"""
    import re
    patterns = [
        r'(\d+)\s*\$',
        r'\$\s*(\d+)', 
        r'до\s+(\d+)\s*\$',
        r'(\d+)\s*долларов'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return f"{match.group(1)}$"
    
    return None

async def show_villa_fork(message: Message, state: FSMContext):
    """Показ развилки выбора виллы"""
    text = get_text("screens.villa_fork.message")
    keyboard = get_keyboard(["📎 Есть ссылка/номер виллы", "🌴 Хочу описать мечту"])
    
    await message.answer(text, reply_markup=keyboard)

    await state.set_state(BotStates.VILLA_FORK)
