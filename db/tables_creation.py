from db_connection import connection, close

import sqlite3


async def t_creation():
    try:
        sqlt_conn, cursor = connection()
        creation_query = """CREATE TABLE users_table (
            ----------
        )"""
    except:
        pass
