import Singleton_import


if __name__ == "__main__":
    obj1 = Singleton_import.SingletonImport()
    obj2 = Singleton_import.SingletonImport()
    print(obj1 is obj2)