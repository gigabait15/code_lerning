import random
import time
import redis


class RateLimitExceed(Exception):
    pass


class RateLimiter:
    def __init__(self, name='rate_limiter', host='localhost', port=6379, db=0, limit=5, window=3):
        """
        :param name: Название ключа для Redis.
        :param host: Хост Redis.
        :param port: Порт Redis.
        :param db: Номер базы данных Redis.
        :param limit: Максимальное количество запросов.
        :param window: Временное окно в секундах.
        """
        self.redis = redis.StrictRedis(host=host, port=port, db=db, decode_responses=True)
        self.name = name
        self.limit = limit
        self.window = window

    def test(self) -> bool:
        """
        Проверяет, можно ли выполнить запрос без превышения лимита.
        :return: True, если лимит не превышен, иначе False.
        """
        # текущее время в милисекундах для точности
        current_time = int(time.time() * 1000)
        pipeline = self.redis.pipeline()

        # Добавление временной метки
        pipeline.zadd(self.name, {str(current_time): current_time})
        # Удаление временной метки, если вышла за пределы временного ограничения
        pipeline.zremrangebyscore(self.name, 0, current_time - self.window * 1000)
        # Количество запросов
        pipeline.zcard(self.name)
        # Время жизни ключа
        pipeline.expire(self.name, self.window)
        _, _, count, _ = pipeline.execute()
        # Проверка количества запросов относительно лимита
        is_allowed = count <= self.limit
        # Инфо работы
        print(f"Количество запросов в окне: {count}, Лимит не превышен: {is_allowed}")
        return is_allowed


def make_api_request(rate_limiter: RateLimiter):
    if not rate_limiter.test():
        raise RateLimitExceed
    else:
        # бизнес-логика
        pass


if __name__ == '__main__':
    rate_limiter = RateLimiter()

    for _ in range(50):
        time.sleep(random.uniform(0.1, 1))

        try:
            make_api_request(rate_limiter)
        except RateLimitExceed as e:
            print("Rate limit exceeded!")
        else:
            print("All good")
