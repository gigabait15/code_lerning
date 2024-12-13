# import threading
#
# def task(name):
#     print(f"Задача {name} началась")
#     print(f"Задача {name} завершена")
#
# thread1 = threading.Thread(target=task, args=("1",))
# thread2 = threading.Thread(target=task, args=("2",))
#
# thread1.start()
# thread2.start()
#
# thread1.join()
# thread2.join()


# import threading
#
# event = threading.Event()
#
# def wait_for_event():
#     print("Ожидание события")
#     event.wait()  # Ждем, пока событие не будет установлено
#     print("Событие установлено")
#
# thread = threading.Thread(target=wait_for_event)
# thread.start()
#
# input("Нажмите Enter для установки события\n")
# event.set()  # Устанавливаем событие, чтобы поток мог продолжить работу
# thread.join()


# from concurrent.futures import ThreadPoolExecutor
#
# def task(name):
#     print(f"Выполнение задачи {name}")
#
# with ThreadPoolExecutor(max_workers=2) as executor:
#     executor.submit(task, "1")
#     executor.submit(task, "2")


from multiprocessing import Process

def compute():
    print("Выполнение процесса")    

process = Process(target=compute)
process.start()
process.join()