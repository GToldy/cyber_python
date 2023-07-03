from os.path import join, dirname, realpath
from util import util
from flask import Flask, render_template, request, redirect, flash, url_for
import data.data_manager as manager
import secrets
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = secrets.token_hex(24)
UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/img')
load_dotenv()


@app.route('/')
def index():
    return render_template('index.html', user_list=[])


@app.route('/face-recognition', methods=['GET', 'POST'])
def face_recognition():
    pass


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    return render_template('registration.html')


@app.route('/api/users/<user_id>', methods=['GET', 'PUT', 'DELETE'])
@app.route('/api/users', methods=['GET', 'POST'])
# @util.json_response
def user_controller(user_id=None):
    if user_id is not None:
        pass
    elif request.method == 'POST':
        userdata = request.form
        if userdata['password'] == userdata['password-check']:
            manager.create_user(userdata)
            return redirect(url_for('index'))
        return redirect(url_for('registration'))
    else:
        users = manager.get_all_users()
        print(users)
        return render_template('index.html', user_list=users)


if __name__ == '__main__':
    app.run()
