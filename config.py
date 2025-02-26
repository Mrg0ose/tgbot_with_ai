import os
from dotenv import load_dotenv
from promts import PROMPT_SMM, PROMPT_ANALYST,PROMPT_PROGRAMMING,PROMPT_RESET

# Загрузка переменных окружения из файла .env
load_dotenv()

# Ваши API ключ и название модели
TELEGRAM_BOT_TOKEN = os.getenv('BOT_TOKEN')
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
MODEL_NAME = 'qwen/qwen2.5-vl-72b-instruct:free'
API_URL = 'https://openrouter.ai/api/v1/chat/completions'
# Промты для кнопок
PROMT_SMM = PROMPT_SMM
PROMT_PROGRAMMIST = PROMPT_PROGRAMMING
PROMT_ANALYST = PROMPT_ANALYST
PROMT_RESET = PROMPT_RESET


