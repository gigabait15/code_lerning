def run_wsgi_app(app, environ):
    def start_response(status, response_headers):
        # Сохраняем статус и заголовки для последующей отправки
        nonlocal status_line, headers
        status_line = status
        headers = response_headers

    # Вызываем WSGI-приложение
    response_body = app(environ, start_response)

    # Формируем HTTP-ответ
    response = [f'HTTP/1.1 {response_body.status_line}'.encode()]
    for header in response_body.headers:
        response.append(f'{header[0]}: {header[1]}'.encode())
    response.append(b'')
    response.extend(response_body)

    return response

# Пример использования
environ = {
    'REQUEST_METHOD': 'GET',
    'PATH_INFO': '/',
    'SERVER_NAME': 'localhost',
    'SERVER_PORT': '8000',
    # Другие необходимые ключи
}

response = run_wsgi_app(simple_app, environ)
print(b'\r\n'.join(response).decode())

# WSGI-приложение
def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return [b"Hello, World!"]