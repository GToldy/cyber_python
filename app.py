from os.path import join, dirname, realpath
import time
import os

import logic.face_detection
from logic import face_detection

from flask import Flask, render_template, request, redirect, flash
from werkzeug.utils import secure_filename

import util

app = Flask(__name__)
app.secret_key = util.generate_random_secret_key()
UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/img')


@app.route('/')
def index():  # put application's code here
    return render_template('index.html')


@app.route('/face-detection', methods=['GET', 'POST'])
def face_detection():
    if request.method == 'POST':
        if 'image' not in request.files:
            flash('No file part')
            return redirect(request.url)
        else:
            image = request.files['image']
            image_file = f'{time.time()}_{image.filename}'
            image_path = '{0}/{1}'.format('./static/img/uploaded', image_file)
            image.save(image_path)
            logic.face_detection.face_detect(image_path)
        return render_template('face-detect.html', image=image_file)
    return render_template('index.html')



if __name__ == '__main__':
    app.run()
