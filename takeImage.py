import cv2
import os

def TakeImage(enrollment, name, cascade_path, save_dir, message_label, err_screen, tts):
    if not enrollment or not name:
        err_screen()
        return

    tts("Capturing face image")
    face_cascade = cv2.CascadeClassifier(cascade_path)
    cam = cv2.VideoCapture(0)

    count = 0
    os.makedirs(save_dir, exist_ok=True)
    filename = f"{save_dir}/{enrollment}_{name}.jpg"

    while True:
        ret, img = cam.read()
        if not ret:
            break
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            count += 1
            face_img = img[y:y+h, x:x+w]
            cv2.imwrite(filename, face_img)
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

        cv2.imshow("Register Face", img)
        if cv2.waitKey(1) == ord('q') or count >= 1:
            break

    cam.release()
    cv2.destroyAllWindows()
    message_label.config(text=f"Image saved for {name}")
    tts("Face image captured successfully")
