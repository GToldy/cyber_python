import base64
import struct

import cv2
import numpy as np
from face_recognition import face_encodings, compare_faces

import face_recognition


def encode_image(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return face_encodings(image)[0]


def pack_face_data(image):
    img_encoding = encode_image(image)
    byte_data = struct.pack('f' * len(img_encoding), *img_encoding)
    return byte_data


def unpack_face_data(byte_data):
    face_encoding = struct.unpack('f' * (len(byte_data) // struct.calcsize('f')), byte_data)
    return face_encoding


def check_faces(user_data, frame_data):
    return compare_faces(user_data, frame_data)


def capture_image(request):
    image_data_url = request.json['image']
    image_data = base64.b64decode(image_data_url.split(',')[1])
    nparr = np.frombuffer(image_data, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
