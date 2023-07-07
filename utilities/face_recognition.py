import cv2
from simple_facerec import SimpleFacerec


def recognise_faces():
    global frame, face_locations, name, key

    # Encode faces from a folder
    sfr = SimpleFacerec()
    sfr.load_encoding_images("static/img/")
    # Load Camera
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()

        # Detect faces
        face_locations, face_names = sfr.detect_known_faces(frame)
        for face_loc, name in zip(face_locations, face_names):
            # top, right, bottom, left = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
            y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
            cv2.putText(frame, name.capitalize(), (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)
        cv2.imshow("Frame", frame)

        key = cv2.waitKey(1)
        if key == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
