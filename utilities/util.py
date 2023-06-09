import argparse
from functools import wraps
from flask import jsonify

from controllers import user_controller
from utilities.security import hash_password, verify_password


def json_response(func):
    """
    Converts the returned dictionary into a JSON response
    :param func:
    :return:
    """
    @wraps(func)
    def decorated_function(*args, **kwargs):
        return jsonify(func(*args, **kwargs))

    return decorated_function


def verify_user_data(session, user_data):
    if 'username' in user_data and len(user_data['username']) < 3:
        return False, 'Username must be 3 characters or more'
    elif 'password_check' in user_data and user_data['password'] != user_data['password_check']:
        return False, 'Passwords do not mach. Try again'
    else:
        if 'user_id' in session:
            return True, 'Data changed successfully'
        return True, 'Registered successfully. Now you are logged in'


def verify_login_data(user_data):
    user = user_controller.get_user_by_username(user_data['username'])
    if user is not None:
        is_valid = verify_password(user_data['password'], user['password'])
        if is_valid:
            return True, user, 'Logged in successfully.'
        else:
            return False, None, 'Incorrect password. Try again'
    else:
        return False, None, 'Incorrect username. Try again'


def unpacked_user_data(user_data):
    user_dictionary = {}
    for key, value in user_data.items():
        user_dictionary[key] = value
    return user_dictionary


def get_hashed_data(user_data_item):
    user_data_item = hash_password(user_data_item)
    return user_data_item


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ip', type=str, default='127.0.0.1', help='Ip address of the device')
    parser.add_argument('-o', '--port', type=int, default=5000, help='Ephemeral port number of the '
                                                                                    'server (1024 to 65535)')
    parser.add_argument("-f", "--frame-count", type=int, default=32, help='# of frames used to construct the '
                                                                          'background model')
    return vars(parser.parse_args())
