from os.path import join, dirname, realpath
from flask import Flask, render_template, request, redirect, flash, url_for, session
import data.data_manager as manager
import secrets
from dotenv import load_dotenv

from controllers import user_controller
from util.util import verify_user_data

app = Flask(__name__)
app.secret_key = secrets.token_hex(24)
UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/img')
load_dotenv()


@app.route('/')
def index():
    username = session['username'] if 'username' in session else None
    return render_template('index.html', user=username)


@app.route('/face-recognition', methods=['GET', 'POST'])
def face_recognition():
    pass


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print(request.form['username'])
        user_data = user_controller.get_user_by_username(request.form['username'])
        print(user_data, "userdata")
        return redirect(url_for('user_profile', user_id=user_data['id']))
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        user_controller.create_user(request.form)
        print(request.form)
        return redirect(url_for('index', user=request.form['username']))
    return render_template('registration.html')


@app.route('/profile/<int:user_id>')
def user_profile(user_id):
    user_data = user_controller.get_user_by_id(user_id)
    return render_template('profile.html', user=user_data)


@app.route('/profile/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_profile(user_id):
    user_data = user_controller.get_user_by_id(user_id)
    if request.method == 'POST':
        is_verified, flash_message = verify_user_data(request.form)
        if is_verified:
            user_controller.update_user(user_id, request.form)
            flash(flash_message, 'info')
            return redirect(url_for('user_profile', user_id=user_id))
        else:
            flash(flash_message, 'error')
            return redirect(url_for('edit_profile', user_id=user_id))
    return render_template('edit_profile.html', user=user_data)


@app.route('/profile/<int:user_id>/delete', methods=['POST'])
def delete_profile(user_id):
    user_controller.delete_user(user_id)
    flash('User successfully deleted. Bye.')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
