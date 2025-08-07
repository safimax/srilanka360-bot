from aiogram.fsm.state import State, StatesGroup

class BotStates(StatesGroup):
    # Приветствие  
    WELCOME_UTM = State()
    WELCOME_CHANNEL = State() 
    WELCOME_EXTERNAL = State()
    QUESTIONS_START = State()
    
    # Развилка и ввод
    VILLA_UTM_DETECTED = State()
    VILLA_FORK = State()
    VILLA_INPUT = State()
    DREAM_FORM = State()
    
    # Основной поток
    GROUP_TYPE = State()
    FAMILY_ADULTS = State()
    FAMILY_CHILDREN = State()
    EVENT_SIZE = State()
    
    # Даты (для будущих итераций)
    DATES_PRECISION = State()
    CONTACT_NAME = State()
    CONTACT_PHONE = State()
    SUMMARY = State()