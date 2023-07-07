from flask import session, flash
import data.data_manager as manager
from utilities import util, security
from utilities.face_encodings import pack_face_data, unpack_face_data, check_faces, encode_image


def get_all_users():
    return manager.get_all_users()


def get_user_by_id(user_id):
    return manager.get_user_by_id(user_id)


def get_user_by_username(user_name):
    return manager.get_user_by_username(user_name)


def check_if_face_data_is_user(username, face_data):
    user_data = manager.get_all_user_data_by_username(username)
    user_db_face_data = user_data['data']
    user_face_data = unpack_face_data(user_db_face_data)
    encoded_frame = encode_image(face_data)
    print(len(user_face_data))
    print(len(encoded_frame))
    return check_faces([user_face_data], encoded_frame)[0], user_data, 'Logged in successfully'


def check_if_user_exists(user_name):
    return manager.check_if_user_exists(user_name)


def create_face_data(username, face_data):
    user_data = manager.get_user_by_username(username)
    face_encoding = pack_face_data(face_data)
    manager.create_face_data(user_data, face_encoding)
    return True, 'Successfully saved face data'


def create_user(user_data):
    user_exists = check_if_user_exists(user_data['username'])
    if user_exists:
        return False, 'Username already exists. Try again'
    else:
        is_verified, flash_message = util.verify_user_data(session, user_data)
        if is_verified:
            simple_user_data = util.unpacked_user_data(user_data)
            simple_user_data['password'] = security.hash_password(simple_user_data['password'])
            manager.create_user(simple_user_data)
            return True, flash_message
        else:
            return False, flash_message


def update_user(user_id, new_data):
    old_data = manager.get_user_by_id(user_id)
    for key, value in new_data.items():
        if key == 'password':
            old_data["password"] = security.hash_password(new_data["password"])
            continue
        old_data[key] = value
    manager.update_user(user_id, old_data)
    session['username'] = old_data['username']


def delete_user(user_id):
    manager.delete_user(user_id)
