from psycopg2 import sql
from data.connection import connection_handler
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


@connection_handler
def create_user(cursor, userdata):
    query = """
    INSERT INTO "Users"
    VALUES (default, %(username)s,%(password)s, %(face_recognition)s);
    """
    cursor.execute(query, {'username': userdata['username'], 'password': userdata['password'],
                           'face_recognition': userdata['face_recognition']})


@connection_handler
def get_all_users(cursor):
    query = """
    SELECT * FROM "Users";
    """
    cursor.execute(query)
    return cursor.fetchall()

