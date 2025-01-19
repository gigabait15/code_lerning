import redis
import datetime
import time
from functools import wraps

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


def single(max_processing_time: datetime.timedelta):
    """
    Декоратор блокировки функции с помощью redis, если она запущена.
    При запуске функции сохраняются данные в redis и если будет повторная попытка, то происходит блокировка отработки
    функции и уведомление в консоль. Как только работы функции заверщается, блокировка снимается и выводится сообщение
    в консоль
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            lock_key = f"lock:{func.__name__}"
            lock_value = f"{time.time()}"
            lock_expiry = int(max_processing_time.total_seconds())

            lock_acquired = redis_client.set(
                lock_key, lock_value, nx=True, ex=lock_expiry
            )

            if not lock_acquired:
                print(f"Функция {func.__name__} уже запущена.")
                return

            try:
                print(f"Функция заблокирована {func.__name__}.")
                return func(*args, **kwargs)
            finally:
                current_value = redis_client.get(lock_key)
                if current_value and current_value.decode() == lock_value:
                    redis_client.delete(lock_key)
                    print(f"Блокировка снята для {func.__name__}.")

        return wrapper

    return decorator

# декорируемая функция, sleep для имитации работы
@single(max_processing_time=datetime.timedelta(minutes=2))
def process_transaction(transaction_id):
    print(f"Обработка транзакции {transaction_id}...")
    time.sleep(5)
    print(f"Транзакция {transaction_id} обработана.")


if __name__ == "__main__":
    # запуск функции в нескольких потоках для проверки отработки декоратора
    import threading

    def worker(transaction_id):
        process_transaction(transaction_id)

    threads = [
        threading.Thread(target=worker, args=(1,)),
        threading.Thread(target=worker, args=(1,)),
        threading.Thread(target=worker, args=(2,)),
    ]

    for t in threads:
        t.start()

    for t in threads:
        t.join()