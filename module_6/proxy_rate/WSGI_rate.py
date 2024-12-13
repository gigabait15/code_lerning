# Задача -  WSGI функция которая проксирует курс валют
import json
import requests
from wsgiref.simple_server import make_server


def currency_proxy(environ, start_response):
    """
    WSGI функция-прокси, которая извлекает валюту из URL, делает запрос к стороннему API для получения
    актуального курса валюты и возвращает результат в формате JSON.

    Параметры:
    environ (dict): Словарь, содержащий информацию о запросе, включая путь и другие параметры.
    start_response (function): Функция для отправки статуса и заголовков HTTP-ответа.

    Возвращаемое значение:
    list: Список байтов, который является телом HTTP-ответа в формате JSON, содержащим курс валюты или
          сообщение об ошибке.
    """
    path = environ.get('PATH_INFO', '').strip('/')
    currency = path.upper()

    url = f"https://api.exchangerate-api.com/v4/latest/{currency}"

    response = requests.get(url)

    status = '200 OK' if response.status_code == 200 else '500 Internal Server Error'
    headers = [('Content-type', 'application/json')]

    if response.status_code == 200:
        body = json.dumps(response.json())
    else:
        body = json.dumps({"error": "Unable to fetch exchange rates"})

    start_response(status, headers)
    return [body.encode('utf-8')]



if __name__ == '__main__':
    httpd = make_server('', 8000, currency_proxy)
    print("Serving on port 8000...")
    httpd.serve_forever()
