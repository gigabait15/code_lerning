# Задача - ASGI  функция которая проксирует курс валют
import httpx
import uvicorn
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

EXCHANGE_RATE_API_URL = "https://api.exchangerate-api.com/v4/latest/{currency}"


async def get_exchange_rate(request):
    """
    Асинхронная функция для получения курса валюты по запросу пользователя. Функция извлекает название валюты из
    URL, отправляет запрос к стороннему API для получения актуального курса и возвращает результат в формате JSON.

    Параметры:
    request (Request): Объект запроса, содержащий параметры пути, включая валюту, для которой нужно получить курс.

    Возвращаемое значение:
    JSONResponse: Объект JSON-ответа, содержащий курсы валют для запрашиваемой валюты или сообщение об ошибке.
    """
    currency = request.path_params['currency']
    url = EXCHANGE_RATE_API_URL.format(currency=currency)

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

        if response.status_code == 200:
            data = response.json()
            data['provider'] = "https://www.exchangerate-api.com"
            data['WARNING_UPGRADE_TO_V6'] = "https://www.exchangerate-api.com/docs/free"
            data['terms'] = "https://www.exchangerate-api.com/terms"
            return JSONResponse(data)
        else:
            return JSONResponse({"error": "Unable to fetch exchange rates"}, status_code=500)



app = Starlette(debug=True, routes=[
    Route('/{currency}', get_exchange_rate),
])

if __name__ == "__main__":
    uvicorn.run("module_6.proxy_rate.ASGI_rate:app", host="localhost", port=8000, reload=True)

