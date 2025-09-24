import cv2
import numpy as np
from PIL import Image
import os

def TrainImage(haarcascade_path, image_path, save_path, message_label, tts):
    # Create LBPH recognizer
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier(haarcascade_path)

    def getImagesAndLabels(path):
        imagePaths = []
        # Walk through all subdirectories under TrainingImage/
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.lower().endswith(("jpg", "jpeg", "png")):
                    imagePaths.append(os.path.join(root, file))

        faces = []
        Ids = []
        for imagePath in imagePaths:
            try:
                # Convert image to grayscale
                img = Image.open(imagePath).convert('L')
                img_numpy = np.array(img, 'uint8')

                # Extract ID from filename: Name.Enrollment.Sample.jpg
                file_name = os.path.split(imagePath)[-1]
                Id = int(file_name.split(".")[1])

                # Detect face in the image
                detected_faces = detector.detectMultiScale(img_numpy)
                for (x, y, w, h) in detected_faces:
                    faces.append(img_numpy[y:y+h, x:x+w])
                    Ids.append(Id)

            except Exception as e:
                print(f"Skipped {imagePath}: {e}")
                continue

        return faces, Ids

    # Get faces and IDs
    faces, Ids = getImagesAndLabels(image_path)

    if len(faces) == 0:
        message_label.config(text="No student images found! Please register faces first.", fg="red")
        tts("No student images found. Please register faces first.")
        return

    # Train the recognizer
    recognizer.train(faces, np.array(Ids))

    # Ensure save directory exists
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    recognizer.save(save_path)

    message_label.config(text="Training Completed Successfully!", fg="green")
    tts("Training completed successfully")
