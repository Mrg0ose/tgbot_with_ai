import logging
from handlers import bot
from logging_config import setup_logging

if __name__ == '__main__':
    logger = setup_logging()
    logger.info('Запуск бота...')
    bot.polling(none_stop=True)