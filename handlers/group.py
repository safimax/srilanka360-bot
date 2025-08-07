from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from states.bot_states import BotStates
from utils.text_utils import get_text, get_keyboard

router = Router()

@router.callback_query(F.data == "семья__компания_друзей")
async def handle_family_group(callback: CallbackQuery, state: FSMContext):
    """Пользователь выбрал семью/друзей"""
    await state.update_data(group_type="family")
    await show_family_adults(callback.message, state)
    await callback.answer()

@router.callback_query(F.data == "мероприятие__йогатур")
async def handle_event_group(callback: CallbackQuery, state: FSMContext):
    """Пользователь выбрал мероприятие/тур"""
    await state.update_data(group_type="event")
    await show_event_size(callback.message, state)
    await callback.answer()

@router.callback_query(F.data.in_(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10+"]))
async def handle_adults_count(callback: CallbackQuery, state: FSMContext):
    """Обработка выбора количества взрослых"""
    adults_count = callback.data
    await state.update_data(adults_count=adults_count)
    
    # Пока что заканчиваем здесь - покажем итоговое сообщение
    data = await state.get_data()
    summary = f"Отлично! Получена заявка:\n\n"
    summary += f"• Источник: {data.get('entry_point', 'Неизвестно')}\n"
    summary += f"• Тип группы: Семья/Друзья\n" 
    summary += f"• Взрослых: {adults_count}\n"
    
    if data.get('villa_id'):
        summary += f"• Интересует вилла: {data['villa_id']}\n"
    if data.get('villa_input_raw'):
        summary += f"• Ссылка на виллу: {data['villa_input_raw']}\n"
    if data.get('dream_description'):
        summary += f"• Описание: {data['dream_description'][:100]}...\n"
        summary += f"• Бюджет: {data.get('budget_mentioned', 'не указан')}\n"
    
    summary += "\n✅ Заявка сохранена! Наш эксперт свяжется с вами в ближайшее время."
    
    keyboard = get_keyboard(["💬 Связаться с экспертом сейчас"])
    await callback.message.edit_text(summary, reply_markup=keyboard)
    await callback.answer()

async def show_group_type(message: Message, state: FSMContext):
    """Показ выбора типа группы"""
    text = get_text("screens.group_type.message")
    keyboard = get_keyboard(["👨‍👩‍👧‍👦 Семья / Компания друзей", "🧘‍♀️ Мероприятие / Йога-тур"])
    
    await message.answer(text, reply_markup=keyboard)
    await state.set_state(BotStates.GROUP_TYPE)

async def show_family_adults(message: Message, state: FSMContext):
    """Показ выбора количества взрослых"""
    text = "Сколько будет взрослых?"
    buttons = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10+"]
    keyboard = get_keyboard(buttons)
    
    await message.answer(text, reply_markup=keyboard)
    await state.set_state(BotStates.FAMILY_ADULTS)

async def show_event_size(message: Message, state: FSMContext):
    """Показ выбора размера мероприятия"""
    text = "На какое примерное количество участников вы ищете виллу?"
    await message.answer(text + "\n\n(Эта функция будет добавлена в следующей версии)")