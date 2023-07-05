from data.connection import connection_handler


@connection_handler
def create_user(cursor, userdata):
    query = """
        INSERT INTO "Users" (username, password, face_recognition)
        VALUES (%(username)s, %(password)s, %(face_recognition)s);
    """
    cursor.execute(query, {'username': userdata['username'],
                           'password': userdata['password'],
                           'face_recognition': userdata['face_recognition']})


@connection_handler
def get_all_users(cursor):
    query = """
        SELECT * FROM "Users";
    """
    cursor.execute(query)
    return cursor.fetchall()


@connection_handler
def get_user_by_id(cursor, user_id):
    query = """
        SELECT * FROM "Users"
        WHERE "Users".id = %(user_id)s
    """
    cursor.execute(query, {'user_id': user_id})
    return cursor.fetchone()


@connection_handler
def get_user_by_username(cursor, user_name):
    query = """
        SELECT * FROM "Users"
        WHERE username = %(username)s
    """
    cursor.execute(query, {'username': user_name})
    return cursor.fetchone()


@connection_handler
def check_if_user_exists(cursor, user_name):
    query = """
        SELECT EXISTS(SELECT 1 FROM "Users" WHERE username = %(user_name)s);
    """
    cursor.execute(query, {'user_name': user_name})
    return cursor.fetchone()['exists']


@connection_handler
def update_user(cursor, user_id, user_data):
    query = """
        UPDATE "Users" SET username = %(user_name)s, password = %(password)s, face_recognition = %(face_recognition)s
        WHERE id = %(user_id)s
    """

    cursor.execute(query, {'user_id': user_id,
                           'user_name': user_data['username'],
                           'password': user_data['password'],
                           'face_recognition': user_data['face_recognition']})


@connection_handler
def delete_user(cursor, user_id):
    query = """
        DELETE FROM "Users"
        WHERE id = %(user_id)s
    """

    cursor.execute(query, {'user_id': user_id})
