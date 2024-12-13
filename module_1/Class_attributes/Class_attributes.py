# метакласс, который автоматически добавляет атрибут created_at с текущей датой и временем к любому классу,
# который его использует
import datetime


class MyMeta(type):
    def __new__(cls, name, bases, attrs):
        """
         Метод __new__ вызывается при создании нового объекта.
         Переопределяется, чтобы контролировать создание экземпляров.
        """
        attrs['created_at'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        return super().__new__(cls, name, bases, attrs)


class MyClass(metaclass=MyMeta):
    pass


if __name__ == '__main__':
    obj = MyClass()
    print(obj.created_at)

