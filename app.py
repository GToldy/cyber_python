from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():  # put application's code here
    return render_template('index.html')


@app.route('/face-recognition', methods=['GET'])
def face_recognition():
    return render_template('face-rec.html')


if __name__ == '__main__':
    app.run()
