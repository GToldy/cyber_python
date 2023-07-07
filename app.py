import json
import mimetypes
import threading
from flask import Flask, render_template, request, redirect, flash, url_for, session

from utilities.face_encodings import capture_image
from utilities.util import verify_user_data, verify_login_data, arg_parser
from os.path import join, dirname, realpath
from controllers import user_controller
from dotenv import load_dotenv
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(24)
mimetypes.add_type('application/javascript', '.js')
UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/img')
load_dotenv()


@app.route('/')
def index():
    username = session['username'] if 'username' in session else None
    return render_template('index.html', user=username)


@app.route('/face-capture', methods=['GET', 'POST'])
def video_feed():
    return render_template('face_capture.html')


@app.route('/save_face_data', methods=['POST'])
def save_face_data():
    image = capture_image(request)
    session.pop('username', None)
    is_success, flash_message = user_controller.create_face_data(request.json['name'], image)
    if is_success:
        session.pop('register', None)
        flash(flash_message, 'info')
        data = {"is_success": is_success}  # Your data in JSON-serializable type
        app.response_class(response=data,
                           status=200,
                           mimetype='application/json')
        return redirect(url_for('login'))
    else:
        print(is_success)
        data = {"is_success": is_success}  # Your data in JSON-serializable type
        app.response_class(response=data,
                           status=404,
                           mimetype='application/json')
        return redirect(url_for('registration'))


@app.route('/check_face_data', methods=['POST'])
def check_face_data():
    image = capture_image(request)
    is_success, user_data, flash_message = user_controller.check_if_face_data_is_user(request.json['name'], image)
    if is_success:
        session.pop('login', None)
        session['user_id'] = user_data['id']
        print('Success : ', is_success)
        flash(flash_message, 'info')
        data = {"is_success": is_success}  # Your data in JSON-serializable type
        app.response_class(response=data,
                           status=200,
                           mimetype='application/json')
        return redirect(url_for('user_profile', user_id=user_data['id']))
    else:
        print('Nope')
        session.pop('user_id', None)
        session.pop('username', None)
        print('Success : ', is_success)
        data = {"is_success": is_success}  # Your data in JSON-serializable type
        app.response_class(response=data,
                           status=404,
                           mimetype='application/json')
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['login'] = True
        is_verified, user_data, flash_message = verify_login_data(request.form)
        if is_verified:
            session['username'] = user_data['username']
            if user_data['face_recognition']:
                return redirect(url_for('video_feed'))
            session['user_id'] = user_data['id']
            session.pop('login', None)
            print(session['user_id'])
            flash(flash_message, 'info')
            return redirect(url_for('user_profile', user_id=user_data['id']))
        else:
            flash(flash_message, 'error')
            return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        session['register'] = True
        is_verified, flash_message = user_controller.create_user(request.form)
        if is_verified:
            if request.form['face_recognition'] == 'True':
                session['username'] = request.form['username']
                return redirect(url_for('video_feed'))
            flash(flash_message, 'info')
            return redirect(url_for('login'))
        flash(flash_message, 'error')
        return redirect(url_for('registration'))
    return render_template('registration.html')


@app.route('/profile/<int:user_id>')
def user_profile(user_id):
    if 'username' in session:
        user_data = user_controller.get_user_by_id(user_id)
        return render_template('profile.html', user=user_data)
    else:
        flash('Please log in to see this profile', 'error')
        return redirect(url_for('login'))


@app.route('/profile/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_profile(user_id):
    user_data = user_controller.get_user_by_id(user_id)
    if request.method == 'POST':
        is_verified, flash_message = verify_user_data(session, request.form)
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
    session.pop('user_id', None)
    session.pop('username', None)
    flash('User successfully deleted. Bye.')
    return redirect(url_for('index'))


if __name__ == '__main__':
    args = arg_parser()

    thread = threading.Thread()
    thread.daemon = True
    thread.start()

    app.run(host=args['ip'], port=args['port'], debug=True, threaded=True, use_reloader=False)
