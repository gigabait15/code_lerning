# Задача - Параллельная обработка числовых данных
import os
import math
import json
import time
import random
import concurrent.futures
import multiprocessing


def generate_data(n):
    """
    Функция генерации списка случайных чисел.
    принимает число в качестве аргумента для указания длины списка
    Возвращает спискок с числовыми элементами
    """
    return [random.randint(1, 1000) for _ in range(n)]

def process_number(number):
    """
    Функция для нахождения факториала числа
    приниммет число в качестве аргумента
    возвращает факториал числа
    """
    return math.factorial(number)

def process_with_single(items):
    """
    Однопоточная функция для вычисления факториалов для всех чисел в списке
    принимет в качестве аргумента список чисел
    возвращает список факториалов чисел
    """
    return list(map(process_number, items))

# Вариант А: Пул потоков с concurrent.futures
def process_with_threads(items):
    """
    Многопоточная функция с использованием  concurrent.futures для вычисления факториалов для всех чисел в списке
    принимет в качестве аргумента список чисел
    возвращает список факториалов чисел
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        return list(executor.map(process_number, items))

# Вариант Б: Пул процессов
def process_with_pool(items):
    """
    Многопроцессорная функция с использованием  multiprocessing.Pool для вычисления факториалов для всех чисел в списке
    принимет в качестве аргумента список чисел
    возвращает список факториалов чисел
    """
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        return pool.map(process_number, items)


# Вариант В: Отдельные процессы с использованием multiprocessing.Process и очередей
def worker(input_queue, output_queue):
    """
    Рабочий процесс, который извлекает числа из очереди,
    вычисляет факториалы и помещает результаты в выходную очередь.
    """
    while True:
        number = input_queue.get()
        if number is None:
            break

        output_queue.put(process_number(number))


def process_with_processes(items):
    """
    Многопроцессорная функция с использованием multiprocessing.Process
    для вычисления факториалов для всех чисел в списке с использованием очередей.
    Принимает в качестве аргумента список чисел.
    Возвращает список факториалов чисел.
    """
    input_queue = multiprocessing.Queue()
    output_queue = multiprocessing.Queue()

    num_processes = multiprocessing.cpu_count()
    processes = []

    for _ in range(num_processes):
        process = multiprocessing.Process(target=worker, args=(input_queue, output_queue))
        processes.append(process)
        process.start()

    for item in items:
        input_queue.put(item)

    for _ in range(num_processes):
        input_queue.put(None)

    results = []
    for _ in range(len(items)):
        results.append(output_queue.get())

    for process in processes:
        process.join()

    return results

def measure_time(func, items):
    """
    Функция для отображения времени работы функции
    Принимает функцию и аргумент для функции в качестве аргументов
    Возвращает время выполнение функции
    """
    start = time.time()
    func(items)
    end = time.time()
    return end - start

def save_results(results, file_path):
    """
    Функция для записи данных в json
    Принимает данные для записи и путь до файла в качестве аргументов
    Создает и записывает данные в файл формата jsonl
    """
    with open(file_path, 'w') as f:
        for result in results:
            json.dump({"result": result}, f)
            f.write("\n")


if __name__ == '__main__':
    data = generate_data(10000)

    # Измерение времени для однопроцессного варианта
    single_thread_time = measure_time(process_with_single, data)

    # Вариант А: Пул потоков
    thread_time = measure_time(process_with_threads, data)

    # Вариант Б: Пул процессов
    pool_time = measure_time(process_with_pool, data)

    # Вариант В: Отдельные процессы
    processes_time = measure_time(process_with_processes, data)

    # Сравнение результатов
    print("Сравнение времени выполнения:")
    print(f"process_with_single: {round(single_thread_time, 4)} секунд")
    print(f"process_with_threads: {round(thread_time, 4)} секунд")
    print(f"process_with_pool: {round(pool_time, 4)} секунд")
    print(f"process_with_processes: {round(processes_time, 4)} секунд")

    # Сохранение результатов в файл
    results = [
        {"method": "process_with_single", "time": single_thread_time},
        {"method": "process_with_threads", "time": thread_time},
        {"method": "process_with_pool", "time": pool_time},
        {"method": "process_with_processes", "time": processes_time}
    ]

    save_results(results, 'results_time.jsonl')
    print("Результаты сохранены в файл 'results_time.jsonl'")
