from flask import flash
import string
from functools import wraps
from flask import jsonify


def json_response(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        return jsonify(func(*args, **kwargs))

    return decorated_function


def verify_user_data(user_data):
    print(user_data)
    if len(user_data['username']) < 3:
        return False, 'Username must be 3 characters or more'
    elif user_data['password'] != user_data['password-check']:
        return False, 'Passwords do not mach. Try again'
    else:
        return True, 'Registered successfully. Now you are logged in'
