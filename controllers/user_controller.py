from flask import session, flash
import data.data_manager as manager
from util import util, security


def get_all_users():
    return manager.get_all_users()


def get_user_by_id(user_id):
    return manager.get_user_by_id(user_id)


def get_user_by_username(user_name):
    return manager.get_user_by_username(user_name)


def check_if_user_exists(user_name):
    return manager.check_if_user_exists(user_name)


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
            user = manager.get_user_by_username(user_data['username'])
            session['user_id'] = user['id']
            session['username'] = simple_user_data['username']
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
