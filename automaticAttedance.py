import cv2
import numpy as np
import face_recognition
import os
import csv
from datetime import datetime

def subjectChoose(tts):
    try:
        tts("Starting attendance process")

        path = 'StudentDetails'
        images = []
        classNames = []

        if not os.path.exists(path):
            tts("StudentDetails folder not found")
            print("❌ Folder 'StudentDetails' not found.")
            return

        myList = os.listdir(path)
        if not myList:
            tts("No student images found")
            print("❌ No images found in StudentDetails.")
            return

        for cl in myList:
            img_path = os.path.join(path, cl)
            img = cv2.imread(img_path)
            if img is None:
                print(f"⚠️ Could not read image: {img_path}")
                continue
            images.append(img)
            classNames.append(os.path.splitext(cl)[0])

        def findEncodings(images):
            encodeList = []
            for img in images:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                encodings = face_recognition.face_encodings(img)
                if encodings:
                    encodeList.append(encodings[0])
                else:
                    print("⚠️ No face found in image.")
            return encodeList

        encodeListKnown = findEncodings(images)
        if not encodeListKnown:
            tts("No valid face encodings found")
            print("❌ No valid face encodings.")
            return

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            tts("Webcam not accessible")
            print("❌ Webcam not accessible.")
            return

        students_marked = set()
        now = datetime.now()
        date_str = now.strftime('%Y-%m-%d')
        time_str = now.strftime('%H:%M:%S')

        os.makedirs('Attendance', exist_ok=True)
        filename = f'Attendance/studentdetails{date_str}.csv'

        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Name', 'Enrollment', 'Time'])

            while True:
                success, img = cap.read()
                if not success:
                    print("❌ Failed to read from webcam.")
                    break

                imgS = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
                imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

                facesCurFrame = face_recognition.face_locations(imgS)
                encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

                for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
                    matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                    faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                    matchIndex = np.argmin(faceDis)

                    if matches[matchIndex]:
                        name = classNames[matchIndex]
                        if name not in students_marked:
                            enrollment, student_name = name.split('_')
                            writer.writerow([student_name, enrollment, time_str])
                            students_marked.add(name)
                            print(f"✅ Marked: {student_name} ({enrollment})")

                        y1, x2, y2, x1 = faceLoc
                        y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(img, student_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

                cv2.imshow('Attendance', img)
                if cv2.waitKey(1) == ord('q'):
                    break

        cap.release()
        cv2.destroyAllWindows()
        tts("Attendance completed")
        print("✅ Attendance completed.")

    except Exception as e:
        tts("An error occurred during attendance")
        print(f"❌ Exception: {e}")
