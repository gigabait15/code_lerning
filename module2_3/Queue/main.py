import threading
import time
from init_db import connect_db as connection


def worker(worker_id: int):
    """
    Функция реализации воркера
    :param worker_id: id назначеннго воркера для задачи
    Данная функция подключается к БД с блокировкой строки для других транзакций,
    в случае если подключение возвращает данные, имитирует работу (метод sleep) и меняет статус задачи на completed.
    Цикл while обеспечивает повтор подключения, в слуае если данные не были получены
    """
    try:
        conn = connection()
        while True:
            with conn.cursor() as cur:
                cur.execute('''SELECT id, status FROM tasks WHERE status = 'processing' AND worker_id = %s
                 FOR UPDATE SKIP LOCKED''', (worker_id,))

                result = cur.fetchone()
                if result is None:
                    print(f"не нашел задачу")
                    time.sleep(1)
                    continue

                task_id, task_status = result
                print(f'Task № {task_id} status {task_status} in working')
                time.sleep(5)

                cur.execute('''UPDATE tasks SET status = 'completed' WHERE id = %s''', (task_id,))
                conn.commit()
                print(f"Task № {task_id} is completed")
                break
    except Exception as ex:
        print(ex)
    finally:
        conn.close()


def fetch_task(task_id, worker_id):
    """
    Функция для назначения воркера и смены статуса у задачи
    :param task_id: id задачи со статусом pending
    :param worker_id: id воркера для назначения задаче
    Функция подключаетмя к БД, находит задачу со статусом pending по указанному id и блокирует поток.
    Далее с помощью методa sleep имитирует работу и меняет статус на processing и назначает воркер для задачи
    """
    conn = connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""SELECT * FROM tasks WHERE status = 'pending' AND id = %s
             FOR UPDATE SKIP LOCKED """, (task_id,))
            time.sleep(1)

            cursor.execute(
                """UPDATE tasks SET status = 'processing', worker_id = %s
                WHERE id = %s RETURNING *;
            """, (worker_id, task_id,)
            )
            conn.commit()
            print(f"Task № {task_id} status {cursor.fetchone()[2]} append worker № {worker_id}")
    except Exception as e:
        print(f'Error {e}')
        conn.rollback()
    finally:
        conn.close()

def len_task():
    """Функция для возврата количества записей в БД"""
    conn = connection()
    with conn.cursor() as cursor:
        cursor.execute('''SELECT COUNT(*) FROM tasks''')
        result = cursor.fetchall()
        return result[0][0]


def main():
    """
    Функция для выполнения согласно ТЗ
    task_ids для получения количества записей(задач) в таблице, worker_threads для хранения потоков выполнения воркера
    Функция проходит по списку с id , fetch_task находит указанную задачу в таблице, меняет статус и назначает воркеру.
    Далее создаются потоки с воркерами и дальнейший запуск
    """
    task_ids = [i for i in range(1, len_task() + 1)]
    worker_threads = []

    for i, task_id in enumerate(task_ids, start=1):
        fetch_task(task_id, worker_id=i)

        worker_thread = threading.Thread(target=worker, args=(i,))
        worker_threads.append(worker_thread)
        worker_thread.start()

    for thread in worker_threads:
        thread.join()

if __name__ == "__main__":
    main()