import csv
from tkinter import *
from tkinter import ttk

def subjectchoose(tts):
    window = Tk()
    window.title("Attendance Records")
    window.geometry("600x400")

    cols = ("Enrollment", "Name", "Date", "Time")
    tree = ttk.Treeview(window, columns=cols, show="headings")
    for col in cols:
        tree.heading(col, text=col)
        tree.pack(fill=BOTH, expand=True)

    with open("studentdetails.csv", "r") as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            tree.insert("", "end", values=row)

    tts("Showing attendance records")
    window.mainloop()
