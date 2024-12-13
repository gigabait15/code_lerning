# декоратор кеширования
import unittest.mock


def lru_cache(maxsize=128):
    """
    Декоратор для кеширования результатов
    :param maxsize: число, которое задает максимальный размер кеша
    """
    def decorator(func):
        cache = {}   # Словарь с аргументами функции в качестве ключа и результат в качестве значения
        order = []  # Список для отслеживания порядка использования ключей

        def wrapped(*args, **kwargs):
            # ключ для кэша
            cache_key = args + tuple(sorted(kwargs.items()))
            if cache_key in cache:
                # Если ключ уже в кэше, перемещаем его в конец списка и вовзращаем результат
                order.remove(cache_key)
                order.append(cache_key)
                return cache[cache_key]
            result = func(*args, **kwargs)
            # Сохраняем результат в кэш
            cache[cache_key] = result
            order.append(cache_key)
            # Если кэш превышает максимальный размер, удаляем недавно использованный элемент
            if len(cache) > maxsize:
                oldest_key = order.pop(0)
                del cache[oldest_key]
            return result

        return wrapped
    return decorator


@lru_cache()
def sum(a: int, b: int) -> int:
    return a + b


@lru_cache()
def sum_many(a: int, b: int, *, c: int, d: int) -> int:
    return a + b + c + d


@lru_cache(maxsize=3)
def multiply(a: int, b: int) -> int:
    return a * b


if __name__ == '__main__':
    assert sum(1, 2) == 3
    assert sum(3, 4) == 7

    assert multiply(1, 2) == 2
    assert multiply(3, 4) == 12

    assert sum_many(1, 2, c=3, d=4) == 10

    mocked_func = unittest.mock.Mock()
    mocked_func.side_effect = [1, 2, 3, 4]

    decorated = lru_cache(maxsize=2)(mocked_func)
    assert decorated(1, 2) == 1
    assert decorated(1, 2) == 1
    assert decorated(3, 4) == 2
    assert decorated(3, 4) == 2
    assert decorated(5, 6) == 3
    assert decorated(5, 6) == 3
    assert decorated(1, 2) == 4
    assert mocked_func.call_count == 4
