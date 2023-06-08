import cv2
import mediapipe as mp
import time

# cap = cv.VideoCapture('d:/Video/2023-04-25 17-34-02.mkv')
cap = cv2.VideoCapture(0)

p_time = 0

mp_draw = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=20)
draw_specs = mp_draw.DrawingSpec(thickness=1, circle_radius=1)

while True:
    success, img = cap.read()
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(img_rgb)

    if results.multi_face_landmarks:
        for face_lms in results.multi_face_landmarks:
            mp_draw.draw_landmarks(img, face_lms, mp_face_mesh.FACEMESH_CONTOURS, draw_specs, draw_specs)
            for lm in face_lms.landmark:
                ih, iw, ic = img.shape
                x, y, z = int(lm.x * iw), int(lm.y * ih), '{:.2f}'.format(lm.z * ic)
                print(x, y, z)

    c_time = time.time()
    fps = int(1 / (c_time - p_time))
    p_time = c_time

    cv2.putText(img, f'FPS: {fps}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
    cv2.imshow('Image', img)
    cv2.waitKey(1)
