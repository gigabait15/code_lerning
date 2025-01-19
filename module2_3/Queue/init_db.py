# Функции для создания БД, таблиц и заполнение таблиц указанными данными
import psycopg2


def create_db():
    """Функция для создания БД"""
    try:
        conn = psycopg2.connect(
            database="postgres",
            user="postgres",
            password="1234",
            host="localhost",
            port="5432"
        )
        conn.autocommit = True

        with conn.cursor() as cur:
            cur.execute("CREATE DATABASE queue_task")
            print("Database 'queue_task' created successfully")
    except psycopg2.errors.DuplicateDatabase:
        print("Database 'queue_task' already exists")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()


def connect_db():
    """Подсключение к рабочей БД"""
    conn = psycopg2.connect(
        database="queue_task",
        user="postgres",
        password="1234",
        host="localhost",
        port="5432"
    )
    return conn


def create_table(connect):
    """
    Функция для создания таблицы с указанными полями
    Также дополнительно реализован триггер на sql, для автоматического обновления поля updated_at
    """
    try:
        with connect.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE tasks (
                    id SERIAL PRIMARY KEY,
                    task_name TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'pending',
                    worker_id INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP  DEFAULT CURRENT_TIMESTAMP
                );
                """
            )

            # тригер для обновления updated_at при внесении измененй в поле
            cur.execute(
                """
                CREATE OR REPLACE FUNCTION update_updated_at_column()
                RETURNS TRIGGER AS $$
                BEGIN
                    NEW.updated_at = CURRENT_TIMESTAMP;
                    RETURN NEW;
                END;
                $$ LANGUAGE plpgsql;
                """
            )
            cur.execute(
                """
                CREATE TRIGGER set_updated_at
                BEFORE UPDATE ON tasks
                FOR EACH ROW
                EXECUTE FUNCTION update_updated_at_column();
                """
            )
            connect.commit()
        print('Created table')
    except Exception as e:
        print(f"Error: {e}")
        connect.rollback()
    finally:
        connect.close()


def add_val_to_table(connect, task_name):
    """
     Функция для заполнение таблицы указанами данными
     task_name: название задачи, обязательно для заполнения
     остальные поля заполняются автоматически
    """
    try:
        with connect.cursor() as cur:
            cur.execute(
                """
                INSERT INTO tasks (task_name)
                VALUES (%s);
                """, (task_name,)
            )
            print(f"Данные успешно добавлены {task_name}")
            connect.commit()
    except Exception as e:
        print(f"Error: {e}")
        connect.rollback()
    finally:
        connect.close()