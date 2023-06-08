from os.path import join, dirname, realpath
import time
from logic import faces_train, face_recognition

from flask import Flask, render_template, request, redirect, flash
from werkzeug.utils import secure_filename

import util

app = Flask(__name__)
app.secret_key = util.generate_random_secret_key()
UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/img')


@app.route('/')
def index():  # put application's code here
    return render_template('index.html')


@app.route('/face-recognition', methods=['GET', 'POST'])
def face_tracking():
    text = ""
    file = ""
    if request.method == 'POST':
        if 'image' not in request.files:
            flash('No file part')
            return redirect(request.url)
        else:
            image = request.files['image']
            image_file = f'{time.time()}_{image.filename}'
            if image.filename != '':
                image.save(join(UPLOAD_FOLDER, secure_filename(image_file)))
                faces_train.faces_train()
                confidence_text, file_name = face_recognition.recognise_uploaded_picture(f'{UPLOAD_FOLDER}/{image_file}')
                return render_template('face-rec.html', text=confidence_text, file=file_name)
            else:
                return redirect('face-rec.html')
    return render_template('face-rec.html', text="", file="")


if __name__ == '__main__':
    app.run()
