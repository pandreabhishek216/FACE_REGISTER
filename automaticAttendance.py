import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import pyttsx3

# Import project modules
import takeImage
import trainImage
import automaticAttedance
import show_attendance

# ---------- Speech Engine ----------
def tts(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# ---------- Error Popup ----------
def err_screen():
    messagebox.showerror("Error", "Enrollment Number and Name are required!")

# ---------- Register Face ----------
def register_face():
    roll = txt_enrollment.get()
    name = txt_name.get()
    takeImage.TakeImage(roll, name, "haarcascade_frontalface_default.xml",
                        "TrainingImage", message_label, err_screen, tts)

# ---------- Train Images ----------
def train_images():
    trainImage.TrainImage("haarcascade_frontalface_default.xml",
                          "TrainingImage", "TrainingImageLabel/Trainner.yml",
                          message_label, tts)

# ---------- Take Attendance ----------
def take_attendance():
    automaticAttedance.subjectChoose(tts)

# ---------- Show Attendance ----------
def show_attendance_records():
    show_attendance.subjectchoose(tts)

# ---------- GUI ----------
root = Tk()
root.title("RAI Technology University Attendance System")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# ---------- Canvas for Gradient Background ----------
canvas = Canvas(root, width=screen_width, height=screen_height)
canvas.pack(fill="both", expand=True)

# Gradient-style blocks
canvas.create_rectangle(0, 0, screen_width, screen_height * 0.25, fill="#FFDEE9", outline="")
canvas.create_rectangle(0, screen_height * 0.25, screen_width, screen_height * 0.5, fill="#B5FFFC", outline="")
canvas.create_rectangle(0, screen_height * 0.5, screen_width, screen_height * 0.75, fill="#C9FFBF", outline="")
canvas.create_rectangle(0, screen_height * 0.75, screen_width, screen_height, fill="#FEEFB3", outline="")

# ---------- Logo (Optional) ----------
try:
    logo_img = Image.open("logo.png")  # Replace with your logo file
    logo_img = logo_img.resize((120, 120), Image.ANTIALIAS)
    logo_photo = ImageTk.PhotoImage(logo_img)
    logo_label = Label(root, image=logo_photo, bg="#FFDEE9")
    logo_label.image = logo_photo
    logo_label.place(x=50, y=30)
except Exception as e:
    print("Logo not found:", e)

# ---------- Title ----------
title = Label(root, text="RAI Technology University Attendance System",
              font=("Times New Roman", 28, "bold"), bg="#FFDEE9", fg="darkblue")
title.place(relx=0.5, y=60, anchor="center")

# ---------- Input Fields ----------
lbl1 = Label(root, text="Enter Your Enrollment Number:", font=("Times New Roman", 18), bg="#B5FFFC")
lbl1.place(x=screen_width * 0.2, y=screen_height * 0.3)
txt_enrollment = Entry(root, font=("Times New Roman", 18), width=30)
txt_enrollment.place(x=screen_width * 0.5, y=screen_height * 0.3)

lbl2 = Label(root, text="Enter Your Name:", font=("Times New Roman", 18), bg="#B5FFFC")
lbl2.place(x=screen_width * 0.2, y=screen_height * 0.35)
txt_name = Entry(root, font=("Times New Roman", 18), width=30)
txt_name.place(x=screen_width * 0.5, y=screen_height * 0.35)

# ---------- Buttons ----------
btn1 = Button(root, text="Register Face", font=("Times New Roman", 16), bg="green", fg="white", command=register_face)
btn1.place(relx=0.5, y=screen_height * 0.45, anchor="center")

btn2 = Button(root, text="Train Images", font=("Times New Roman", 16), bg="orange", fg="white", command=train_images)
btn2.place(relx=0.5, y=screen_height * 0.52, anchor="center")

btn3 = Button(root, text="Take Attendance", font=("Times New Roman", 16), bg="blue", fg="white", command=take_attendance)
btn3.place(relx=0.5, y=screen_height * 0.59, anchor="center")

btn4 = Button(root, text="Show Attendance", font=("Times New Roman", 16), bg="purple", fg="white", command=show_attendance_records)
btn4.place(relx=0.5, y=screen_height * 0.66, anchor="center")

# ---------- Status Message ----------
message_label = Label(root, text="", font=("Times New Roman", 16), bg="#FEEFB3", fg="red")
message_label.place(relx=0.5, y=screen_height * 0.75, anchor="center")

root.mainloop()