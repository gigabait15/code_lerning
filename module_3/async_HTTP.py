# Задача - Асинхронный HTTP-запрос
import aiohttp
import asyncio
import json


urls = [
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url"
]


async def fetch_url(session, url, semaphore):
    """
    Асинхронная функция для выполнения HTTP-запроса для каждого URL
    Используется aiohttp.ClientSession.get() для получения ответа.
     В случае ошибки (например, если сервер недоступен или возникает тайм-аут), возвращается статус код 0.
    """
    try:
        async with semaphore, session.get(url, timeout=10) as response:
            return url, response.status
    except (aiohttp.ClientError, asyncio.TimeoutError):
        return url, 0


async def fetch_urls(items: list[str], file_path: str):
    """
     Асинхронная функция, которая принимает список URL и путь к файлу для записи результатов.
    Используется asyncio.Semaphore для ограничения числа одновременных запросов.
     Все запросы выполняются параллельно с помощью asyncio.gather, и результаты сохраняются в файл в формате JSONL.
    """
    # Ограничение на количество одновременных запросов
    semaphore = asyncio.Semaphore(5)

    async with aiohttp.ClientSession() as session:
        # Список асинхронных задач для каждого URL
        tasks = [fetch_url(session, url, semaphore) for url in items]
        results = await asyncio.gather(*tasks)

        with open(file_path, 'w') as f:
            for url, status_code in results:
                json.dump({"url": url, "status_code": status_code}, f)
                f.write("\n")


if __name__ == '__main__':
    asyncio.run(fetch_urls(urls, './results.jsonl'))