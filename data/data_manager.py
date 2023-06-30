from psycopg2 import sql
import connection
import bcrypt


def hash_password(plain_text_password):
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    if hashed_password is None:
        return False
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


# @connection.connection_handler
# def get_questions(cursor, order_by, order_direction):
#     query = """SELECT * FROM question
#     ORDER BY {} {};"""
#     cursor.execute(sql.SQL(query).format(sql.Identifier(order_by), sql.SQL(order_direction)))
#     return cursor.fetchall()
