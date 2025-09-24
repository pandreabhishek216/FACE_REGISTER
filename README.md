Project Overview
This project, named "RAI Technology University Attendance System", is a desktop application that uses face recognition to automate the process of taking student attendance. It is built using Python and several computer vision and machine learning libraries. The system is designed to be user-friendly, with a graphical interface (GUI) for managing student data and attendance records.


Core Components
1. File Structure and Dependencies
The project is organized into several Python files and directories:

automaticAttendance.py: This is the main script that launches the GUI. It contains the logic for the user interface and calls functions from the other modules.

takeImage.py: This script handles the process of registering a new student. It captures an image from the webcam and saves it for training the face recognition model.

trainImage.py: This module is responsible for training the face recognition model using the captured images.

automaticAttedance.py: This script contains the logic for the real-time attendance system. It uses the trained model to recognize faces and mark attendance.

show_attendance.py: This module is used to display the attendance records from the CSV files in a new window.

haarcascade_frontalface_default.xml: This is an XML file that contains the data for the Haar Cascade Classifier, a machine learning-based approach to detect objects, in this case, a frontal face.

logo.png: An image file used for the application's logo.

requirements.txt: Lists all the necessary Python libraries and their specific versions for the project to run correctly.



2. Workflow
The system follows a logical sequence of operations:

GUI Launch: The automaticAttendance.py script starts the application's main window using Tkinter. The window has fields for a student's enrollment number and name, and buttons for different functions like registering faces, training, taking attendance, and viewing records.

Registering a Face: When a user enters a student's information and clicks the "Register Face" button, the takeImage.py script is called. It opens the webcam and uses the Haar Cascade classifier to find faces. It then captures and saves a single image of the student's face in a designated directory.

Training the Images: After new faces are registered, the "Train Images" button is used to call a function in trainImage.py. This script reads all the saved student images, processes them, and creates a trained model. This model, often saved as a .yml file, stores the unique features of each student's face.

Taking Attendance: When the "Take Attendance" button is clicked, the automaticAttedance.py script starts the webcam. It loads the trained model and continuously scans the video feed for faces. When it recognizes a face, it checks its database to see if the student has already been marked as present for the day. If not, it marks their attendance in a CSV file and displays their name on the screen.

Viewing Records: The "Show Attendance" button executes the show_attendance.py script. This script reads the attendance data from the generated CSV files and displays it in a clean, organized table using a Tkinter Treeview widget.
