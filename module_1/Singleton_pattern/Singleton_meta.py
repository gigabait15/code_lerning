# Синглтон через метакласс

class SingletonMeta(type):
    # приватное поле класса, которое будет хранить единственный экземпляр класса
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        переопределен метод, чтобы контролировать создание экземпляра класса.
        Если экземпляр уже существует, мы просто возвращаем его.
        """
        if cls not in cls._instances:
            # Если экземпляра нет, создаем его
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        # возвращаем существующий или только что созданный экземпляр класса
        return cls._instances[cls]

# Класс синглтона использует метакласс SingletonMeta
class SingletonClass(metaclass=SingletonMeta):
    def __init__(self):
        """
        иницилизация класса
        """
        print("Экземпляр создан.")


if __name__ == "__main__":
    obj1 = SingletonClass()
    obj2 = SingletonClass()
    print(obj1 is obj2)