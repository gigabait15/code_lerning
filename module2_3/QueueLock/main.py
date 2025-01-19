import redis
import json


class RedisQueue:
    def __init__(self, name='default_queue', host='localhost', port=6379, db=0):
        """
        :param name: Название ключа для Redis.
        :param host: Хост Redis.
        :param port: Порт Redis.
        :param db: Номер базы данных Redis.
        """
        self.redis = redis.StrictRedis(host=host, port=port, db=db, decode_responses=True)
        self.name = name

    def publish(self, msg: dict):
        """
        Добавление в очередь.
        В случае если передан не словарь вызывает исключения, если переданные данные коректны добавляет элемент в конец
        очереди и уведомляет в консоль
        :param msg: словарь данных, который нужно добавить в очередь
        """
        if not isinstance(msg, dict):
            raise ValueError("Сообщение должно быть словарем.")
        self.redis.rpush(self.name, json.dumps(msg))
        print(f'{msg} добавлен в очередь')

    def consume(self) -> dict:
        """
        Удаление из очереди.
        В случае если очередь пусты вызывает исключение, если в очереди есть элементы, то удаляет крайний левый элемент
        из очереди, так как это первый элемент добавленный в очередь
        """
        msg = self.redis.lpop(self.name)
        print(f'{msg} удален из очереди')
        if msg:
            return json.loads(msg)
        raise IndexError("Очередь пуста.")


if __name__ == '__main__':
    q = RedisQueue()
    q.publish({'a': 1})
    q.publish({'b': 2})
    q.publish({'c': 3})

    assert q.consume() == {'a': 1}
    assert q.consume() == {'b': 2}
    assert q.consume() == {'c': 3}
