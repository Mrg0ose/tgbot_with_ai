from config import TELEGRAM_BOT_TOKEN, OPENROUTER_API_KEY, MODEL_NAME, API_URL, PROMT_RESET, PROMT_PROGRAMMIST, \
    PROMT_SMM, PROMT_ANALYST
from utils import send_request_to_api
import telebot

# Создание экземпляра бота
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Хранилище контекста диалога
conversation_context = {}

# Словарь для отслеживания статуса обработки запросов
processing_status = {}


# Функция для отправки длинных сообщений
def send_long_message(chat_id, text):
    """
    Разбивает длинное сообщение на части и отправляет каждую часть отдельно.
    """
    max_length = 4096  # Максимальная длина одного сообщения в Telegram
    parts = [text[i:i + max_length] for i in range(0, len(text), max_length)]
    for part in parts:
        bot.send_message(chat_id, part)


# Функция для показа статуса работы бота
def show_bot_status(chat_id):
    """
    Показывает статус "typing" и отправляет временное сообщение,
    если обработка занимает больше времени.
    """
    bot.send_chat_action(chat_id, action='typing')  # Показываем, что бот печатает


# Проверка статуса обработки
def is_processing(chat_id):
    return processing_status.get(chat_id, False)


# Установка статуса обработки
def set_processing(chat_id, status):
    processing_status[chat_id] = status


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    conversation_context[chat_id] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
    set_processing(chat_id, False)  # Сбрасываем статус обработки при старте
    bot.reply_to(message, 'Привет! Я ваш чат-бот. Введите ваш запрос.')


# Общая функция для обработки специальных команд
def handle_special_command(command_name, prompt, message):
    chat_id = message.chat.id

    # Проверяем, обрабатывается ли уже другой запрос
    if is_processing(chat_id):
        bot.reply_to(message, f'Подождите, я еще обрабатываю предыдущий запрос. Пожалуйста, попробуйте позже.')
        return

    # Устанавливаем флаг обработки
    set_processing(chat_id, True)

    user_input = prompt
    conversation_context.setdefault(chat_id, [
        {"role": "system", "content": "You are a helpful assistant."}
    ]).append({'role': 'user', 'content': user_input})

    # Отправляем сообщение о начале обработки
    bot.reply_to(message, f'Накладываю на себя промт {command_name}...')

    # Показываем статус "typing"
    show_bot_status(chat_id)

    headers = {
        'Authorization': f'Bearer {OPENROUTER_API_KEY}',
        'Content-Type': 'application/json',
    }
    payload = {
        'model': MODEL_NAME,
        'messages': conversation_context[chat_id],
    }

    try:
        # Отправляем запрос к API
        response_data = send_request_to_api(API_URL, headers, payload)

        if 'error' in response_data:
            bot.send_message(chat_id, response_data['error'])
        else:
            answer = response_data.get('choices', [{}])[0].get('message', {}).get('content', 'Ответ не найден.')

            # Добавление ответа модели в контекст диалога
            conversation_context[chat_id].append({'role': 'assistant', 'content': answer})

            # Отправляем ответ пользователю, разбивая его при необходимости
            send_long_message(chat_id, answer)
    finally:
        # Сбрасываем флаг обработки независимо от результата
        set_processing(chat_id, False)


# Обработчики специальных команд
@bot.message_handler(commands=['programmer'])
def programmer(message):
    handle_special_command('программиста', PROMT_PROGRAMMIST, message)


@bot.message_handler(commands=['smm'])
def smm(message):
    handle_special_command('СММ', PROMT_SMM, message)


@bot.message_handler(commands=['analyst'])
def analyst(message):
    handle_special_command('аналитика', PROMT_ANALYST, message)


@bot.message_handler(commands=['reset'])
def reset(message):
    handle_special_command('сброса', PROMT_RESET, message)


# Обработчик обычных сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id

    # Проверяем, обрабатывается ли уже другой запрос
    if is_processing(chat_id):
        bot.reply_to(message, 'Подождите, я еще обрабатываю предыдущий запрос. Пожалуйста, попробуйте позже.')
        return

    # Устанавливаем флаг обработки
    set_processing(chat_id, True)

    user_input = message.text
    conversation_context.setdefault(chat_id, [
        {"role": "system", "content": "You are a helpful assistant."}
    ]).append({'role': 'user', 'content': user_input})

    # Показываем статус "typing"
    show_bot_status(chat_id)

    headers = {
        'Authorization': f'Bearer {OPENROUTER_API_KEY}',
        'Content-Type': 'application/json',
    }
    payload = {
        'model': MODEL_NAME,
        'messages': conversation_context[chat_id],
    }

    try:
        # Отправляем запрос к API
        response_data = send_request_to_api(API_URL, headers, payload)

        if 'error' in response_data:
            bot.send_message(chat_id, response_data['error'])
        else:
            answer = response_data.get('choices', [{}])[0].get('message', {}).get('content', 'Ответ не найден.')

            # Добавление ответа модели в контекст диалога
            conversation_context[chat_id].append({'role': 'assistant', 'content': answer})

            # Отправляем ответ пользователю, разбивая его при необходимости
            send_long_message(chat_id, answer)
    finally:
        # Сбрасываем флаг обработки независимо от результата
        set_processing(chat_id, False)