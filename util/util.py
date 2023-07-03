import random
import string
from functools import wraps
from flask import jsonify



def json_response(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        return jsonify(func(*args, **kwargs))

    return decorated_function

