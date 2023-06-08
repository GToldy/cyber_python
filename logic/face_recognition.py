import cv2 as cv
import numpy as np
import time


def recognise_uploaded_picture(path):
    img = cv.imread(path)
    return predict_person(img)


def get_trained_data():
    np.load("features.npy", allow_pickle=True)
    np.load("labels.npy", allow_pickle=True)
    face_recognizer = cv.face.LBPHFaceRecognizer_create()
    face_recognizer.read('trained_faces.yml')
    return face_recognizer


def prepare_picture_for_detection(image):
    # gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    return image


def write_result_to_picture(img, confidence_of_value, label, x, y, w, h):
    print(label)
    text = f'{label} with confidence of {confidence_of_value}%'
    img = cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return text, img


def predict_person(image):
    haar_cascade = cv.CascadeClassifier('logic/haar_cascade.xml')
    face_recogniser = get_trained_data()
    prepared_img = prepare_picture_for_detection(image)
    faces_rectangle = haar_cascade.detectMultiScale(image, 1.1, 5)
    confidence_text = ""
    file_name = f'{time.time()}.jpg'

    for (x, y, w, h) in faces_rectangle:

        faces_of_interest = prepared_img[y:y + w, x:x + h]

        label, confidence_of_value = face_recogniser.predict(faces_of_interest)

        confidence_text, image = write_result_to_picture(image, confidence_of_value, label, x, y, w, h)
        print(image)

    # cv.imwrite(file_name, image)

    return confidence_text, file_name
