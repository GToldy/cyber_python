from os.path import join, dirname, realpath
from util import util
from flask import Flask, render_template, request, redirect, flash

app = Flask(__name__)
app.secret_key = util.generate_random_secret_key()
UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/img')


@app.route('/')
def index():  # put application's code here
    return render_template('index.html')


@app.route('/face-recognition', methods=['GET', 'POST'])
def face_recognition():
    pass


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    return render_template('registration.html')


if __name__ == '__main__':
    app.run()
