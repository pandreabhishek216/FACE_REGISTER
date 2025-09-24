import cv2
import numpy as np
import face_recognition
import os
import csv
from datetime import datetime

# Load known faces
path = 'StudentDetails'
images = []
classNames = []
myList = os.listdir(path)

for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodeList.append(face_recognition.face_encodings(img)[0])
    return encodeList

encodeListKnown = findEncodings(images)

# Start webcam
cap = cv2.VideoCapture(0)

students_marked = set()
now = datetime.now()
date_str = now.strftime('%Y-%m-%d')
time_str = now.strftime('%H:%M:%S')

filename = f'Attendance/studentdetails{date_str}.csv'
os.makedirs('Attendance', exist_ok=True)

with open(filename, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Name', 'Enrollment', 'Time'])

    while True:
        success, img = cap.read()
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

                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(img, student_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow('Webcam', img)
        if cv2.waitKey(1) == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
