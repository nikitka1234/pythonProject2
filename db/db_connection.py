import sqlite3


async def connection(db_name: str = 'client_db') -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    try:
        sqlt_conn = sqlite3.connect(db_name)
        cursor = sqlt_conn.cursor()

    except sqlite3.Error as e:
        print('ConnectionError:', e)

    else:
        print('Connection Success')
        return sqlt_conn, cursor


async def close(sqlt_conn, cursor):
    try:
        cursor.close()
        sqlt_conn.close()

    except sqlite3.Error as e:
        print('CloseError:', e)

    else:
        print('Close Success')
