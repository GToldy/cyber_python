import os
import numpy as np
import cv2 as cv

haar_cascade = cv.CascadeClassifier('haar_cascade.xml')


people = []
DIR = 'FaceTrainingPhotos'

features = []
labels = []


def get_photos():
    for i in os.listdir(DIR):
        people.append(i)


def get_faces_from_photos():
    for person in people:
        path = os.path.join(DIR, person)
        label = people.index(person)

        for img in os.listdir(path):
            img_path = os.path.join(path, img)

            img_array = cv.imread(img_path)
            gray = cv.cvtColor(img_array, cv.COLOR_BGR2GRAY)

            faces_rectangle = haar_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)

            for (x, y, w, h) in faces_rectangle:
                faces_region_of_interest = gray[y:y + h, x:x + w]
                features.append(faces_region_of_interest)
                labels.append(label)


def train(face_features, face_labels):
    features = np.array(face_features, dtype='object')
    labels = np.array(face_labels)

    face_recognizer = cv.face.LBPHFaceRecognizer_create()
    face_recognizer.train(features, labels)

    face_recognizer.save('face_trained.yml')
    np.save('features.npy', features)
    np.save('labels.npy', labels)


get_photos()
get_faces_from_photos()
train(features, labels)
print("Train completed")
