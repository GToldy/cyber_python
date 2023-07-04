from flask import flash
import string
from functools import wraps
from flask import jsonify

from util.security import hash_password


def json_response(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        return jsonify(func(*args, **kwargs))

    return decorated_function


def verify_user_data(user_data):
    if len(user_data['username']) < 3:
        return False, 'Username must be 3 characters or more'
    elif user_data['password'] != user_data['password_check']:
        return False, 'Passwords do not mach. Try again'
    else:
        return True, 'Registered successfully. Now you are logged in'


def unpacked_user_data(user_data):
    user_dictionary = {}
    for key, value in user_data.items():
        user_dictionary[key] = value
    return user_dictionary


def get_hashed_data(user_data_item):
    user_data_item = hash_password(user_data_item)
    return user_data_item

