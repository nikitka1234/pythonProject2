import sqlite3


# Подключаем базу данных и создаем курсор для работы с таблицами
conn = sqlite3.connect('/home/telegram_bot/TELEGRAM_HTR_BOT/db/db.db', check_same_thread=False)
cursor = conn.cursor()


# Функция для работы с таблицей
async def db_table_val(user_id: int, user_name: str, user_surname: str, username: str, photo_number: int = 0) -> None:
    cursor.execute('INSERT INTO test_user_table (user_id, user_name, user_surname, username, photo_number)\
                    VALUES (?, ?, ?, ?, ?)',
                   (user_id, user_name, user_surname, username, photo_number))
    conn.commit()


async def is_user_exist(user_id: int) -> list:
    return list(cursor.execute(f'SELECT EXISTS(SELECT user_id FROM test_user_table WHERE user_id = {user_id})'))[0][0]


# # Эти методы нужны для работы с object storage
# async def get_photo_number(user_id: int):
#     cursor.execute(f'SELECT photo_number FROM test_user_table WHERE user_id = {user_id}')
#     result = cursor.fetchall()[0][0]
#
#     return result
#
#
# async def update_photo_number(user_id: int):
#     cursor.execute(f'UPDATE test_user_table SET photo_number = photo_number + 1 WHERE user_id = {user_id}')
#     conn.commit()
