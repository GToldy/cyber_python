import cv2 as cv
import numpy as np

haar_cascade = cv.CascadeClassifier('haar_cascade.xml')


def recognise_uploaded_picture(path):
    img = cv.imread(path)
    predict_person(img)
    return img


def get_trained_data():
    np.load("features.npy", allow_pickle=True)
    np.load("labels.npy", allow_pickle=True)
    face_recognizer = cv.face.LBPHFaceRecognizer_create()
    face_recognizer.read('trained_faces.yml')
    return face_recognizer


def prepare_picture_for_detection(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    return gray


def write_result_to_picture(img, confidence_of_value, label, x, y, w, h):
    cv.putText(img, str(label) + f' with confidence of {confidence_of_value}%', (20, 20),
               cv.FONT_HERSHEY_COMPLEX, 1.1, (0, 255, 0), thickness=2)
    print(label)
    cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)


def predict_person(image):
    face_recogniser = get_trained_data()
    prepared_img = prepare_picture_for_detection(image)
    faces_rectangle = haar_cascade.detectMultiScale(image, 1.1, 5)

    for (x, y, w, h) in faces_rectangle:
        faces_of_interest = prepared_img[y:y + w, x:x + h]

        label, confidence_of_value = face_recogniser.predict(faces_of_interest)

        write_result_to_picture(image,  confidence_of_value, label, x, y, w, h)

