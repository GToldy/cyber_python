import cv2 as cv


def face_detect(image):
    img = cv.imread(image)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    haar_cascade = cv.CascadeClassifier("logic/haar_cascade.xml")
    faces_rect = haar_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    print(f"Number of faces found = {len(faces_rect)}")

    for x, y, w, h in faces_rect:
        cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), thickness=2)

    cv.imwrite("./static/img/detected/detected_face.jpg", img)
