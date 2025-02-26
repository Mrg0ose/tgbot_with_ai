import requests
import logging

logger = logging.getLogger(__name__)

def send_request_to_api(api_url, headers, payload):
    try:
        logger.debug(f'Отправляю запрос к API: {api_url}')
        logger.debug(f'Заголовки: {headers}')
        logger.debug(f'Полезная нагрузка: {payload}')
        response = requests.post(api_url, headers=headers, json=payload)
        logger.debug(f'Ответ от API: {response.status_code}')
        logger.debug(f'Тело ответа: {response.text}')
        response.raise_for_status()  # Проверка на ошибки HTTP
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 429:
            logger.error(f'Ошибка 429: {http_err}')
            return {'error': 'Вы исчерпали свой текущий лимит запросов.'}
        else:
            logger.error(f'HTTP ошибка: {http_err}')
            return {'error': f'HTTP ошибка: {http_err}'}
    except requests.exceptions.RequestException as req_err:
        logger.error(f'Ошибка запроса: {req_err}')
        return {'error': f'Ошибка запроса: {req_err}'}
    except Exception as e:
        logger.error(f'Неизвестная ошибка: {e}')
        return {'error': f'Неизвестная ошибка: {e}'}