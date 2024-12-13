# декоратор для проверки роли
def access_control(roles: list = None):
    """
    Декоратор для проверки ролей пользователя.
    :param roles: Список ролей, которым разрешен доступ
    """
    # Если роли не переданы, то нет ограничений
    if roles is None:
        roles = []

    def decorator(func):
        def wrapper(*args, **kwargs):
            global current_user_role
            if current_user_role in roles or len(roles) == 0:
                # Если роль подходит или роли не заданы, выполняем функцию
                return func(*args, **kwargs)
            # Если роль пользователя не подходит, выбрасываем исключение
            raise PermissionError(f"Доступ запрещен для роли '{current_user_role}'. Требуются роли: {roles}")

        return wrapper

    return decorator



if __name__ == '__main__':
    @access_control(roles=['admin', 'moderator'])
    def foo():
        print("Доступ к функции")

    # Вызов функции с ограничениями по ролям, роль 'guest' проверка ограничения
    current_user_role = 'guest'
    try:
        foo()
    except PermissionError as e:
        print(e)

    # Вызов функции с ограничениями по ролям, роль 'admin' проверка доступа
    current_user_role = 'admin'
    try:
        foo()
    except PermissionError as e:
        print(e)


    @access_control()
    def foo():
        print("Доступ к функции")


    # Вызов функции без ограничений
    current_user_role = 'noname'
    try:
        foo()
    except PermissionError as e:
        print(e)
