from flask import session, flash
import data.data_manager as manager
from util import util, security

def get_all_users():
    return manager.get_all_users()


def get_user_by_id(user_id):
    return manager.get_user_by_id(user_id)


def get_user_by_username(user_name):
    print(manager.get_user_by_username(user_name))
    return manager.get_user_by_username(user_name)

def create_user(user_data):
    is_verified, flash_message = util.verify_user_data(user_data)
    if is_verified:
        simple_user_data = util.unpacked_user_data(user_data)
        simple_user_data['password'] = security.hash_password(simple_user_data['password'])
        print(simple_user_data)
        manager.create_user(simple_user_data)
        session['username'] = simple_user_data['username']
        flash(flash_message, 'info')
    else:
        flash(flash_message, 'error')


def update_user(user_id, new_data):
    old_data = manager.get_user_by_id(user_id)
    for key, value in new_data.items():
        old_data[key] = value if value else old_data[key]
    old_data["password"] = security.hash_password(old_data["password"])
    manager.update_user(user_id, old_data)
    session['username'] = old_data['username']

def delete_user(user_id):
    manager.delete_user(user_id)
