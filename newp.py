import tkinter as tk
from tkinter import Label
import firebase_admin
from firebase_admin import credentials, db
import cv2
import os
import shutil
import csv
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time
import tkinter.font as font

# Initialize Firebase Admin SDK
cred = credentials.Certificate("path/to/your/serviceAccountKey.json")  # Replace with your Firebase service account key
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://my-first-project-75585-default-rtdb.firebaseio.com/'
})

window = tk.Tk()
window.title("AUTOMATED CRIMINAL IDENTIFICATION SYSTEM")
window.geometry('1368x768')

# Background Image
img = ImageTk.PhotoImage(Image.open("./images/9.jpg"))
panel = Label(window, image=img)
panel.place(x=0, y=0)

# Labels and Input Fields
def create_label(text, x, y):
    return tk.Label(window, text=text, width=20, height=1, fg="white", bg="#496E7C", font=('times', 15, 'bold')).place(x=x, y=y)

def create_entry(x, y):
    return tk.Entry(window, width=20, bg="#ced5db", fg="black", font=('times', 15, 'bold')).place(x=x, y=y)

create_label("Enter ID", 100, 200)
txt = create_entry(400, 200)

create_label("Enter Name", 100, 250)
txt2 = create_entry(400, 250)

create_label("Enter Age", 100, 300)
txt3 = create_entry(400, 300)

create_label("Enter Gender", 100, 350)
txt4 = create_entry(400, 350)

create_label("Notification", 200, 475)
message = tk.Label(window, text="", bg="#ced5db", fg="black", width=50, height=2, activebackground="yellow", font=('times', 15, 'bold'))
message.place(x=400, y=475)

create_label("Criminal Reports", 200, 550)
message2 = tk.Label(window, text="", fg="black", bg="#ced5db", activeforeground="green", width=50, height=3, font=('times', 15, 'bold'))
message2.place(x=400, y=550)

# Functions
def clear():
    txt.delete(0, 'end')
    txt2.delete(0, 'end')
    txt3.delete(0, 'end')
    txt4.delete(0, 'end')
    message.configure(text="")

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    return False

def TakeImages():
    Id = txt.get()
    name = txt2.get()
    age = txt3.get()
    gender = txt4.get()

    if is_number(Id) and name.isalpha():
        cam = cv2.VideoCapture(0)
        detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        sampleNum = 0

        while True:
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                sampleNum += 1
                cv2.imwrite(f"Capturing_Images/{name}.{Id}.{sampleNum}.jpg", gray[y:y + h, x:x + w])
                cv2.imshow('frame', img)

            if cv2.waitKey(100) & 0xFF == ord('q') or sampleNum > 60:
                break

        cam.release()
        cv2.destroyAllWindows()

        row = [Id, name, age, gender]
        with open('Wanted_List/Wanted_List.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)

        message.configure(text=f"Images Saved for ID: {Id} Name: {name} Age: {age} Gender: {gender}")
    else:
        message.configure(text="Enter Valid ID and Name")

def TrainImages():
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    faces, Id = getImagesAndLabels("Capturing_Images")
    recognizer.train(faces, np.array(Id))
    recognizer.save("Models/Trainner.yml")
    message.configure(text="Images Trained")

def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faces = []
    Ids = []

    for imagePath in imagePaths:
        pilImage = Image.open(imagePath).convert('L')
        imageNp = np.array(pilImage, 'uint8')
        Id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces.append(imageNp)
        Ids.append(Id)

    return faces, Ids

def update_firebase_data(name, location, timeStamp, date):
    ref = db.reference('/criminal')  # Reference to the root path
    data = {
        'Name': name,
        'Location': location,
        'Time': timeStamp,
        'Date': date
    }
    ref.push(data)

def TrackImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("Models/Trainner.yml")
    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    df = pd.read_csv("Wanted_List/Wanted_List.csv")
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    attendance = pd.DataFrame(columns=['Id', 'Name', 'Date', 'Time', 'Location'])

    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
            Id, conf = recognizer.predict(gray[y:y + h, x:x + w])

            if conf < 50:
                Location = "chennai_Airport"
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa = df.loc[df['Id'] == Id]['Name'].values
                tt = f"{Id}-{aa}-WANTED"
                attendance.loc[len(attendance)] = [Id, aa, date, timeStamp, Location]
            else:
                Id = 'Non-Criminal'
                tt = str(Id)

            if conf > 75:
                noOfFile = len(os.listdir("Database")) + 1
                cv2.imwrite(f"Database/Image{noOfFile}.jpg", im[y:y + h, x + w])

            cv2.putText(im, str(tt), (x, y + h), font, 1, (255, 255, 255), 2)

        attendance = attendance.drop_duplicates(subset=['Id'], keep='first')
        cv2.imshow('Face_Recognize', im)

        if cv2.waitKey(1) == ord('q'):
            break

    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    Hour, Minute, Second = timeStamp.split(":")
    fileName = f"Criminal_Reports/criminals_{date}_{Hour}-{Minute}-{Second}.csv"
    attendance.to_csv(fileName, index=False)

    cam.release()
    cv2.destroyAllWindows()

    message2.configure(text=attendance)

    # Update Firebase with criminal information
    update_firebase_data(aa[0], Location, timeStamp, date)  # Push data to Firebase

# Buttons
clearButton = tk.Button(window, text="Clear", command=clear, fg="white", bg="#496E7C", width=10, height=1, activebackground="white", font=('times', 15, 'bold'))
clearButton.place(x=300, y=400)

takeImg = tk.Button(window, text="Take Images", command=TakeImages, fg="white", bg="#496E7C", width=15, height=2, activebackground="white", font=('times', 15, 'bold'))
takeImg.place(x=750, y=200)

trainImg = tk.Button(window, text="Train Images", command=TrainImages, fg="white", bg="#496E7C", width=15, height=2, activebackground="white", font=('times', 15, 'bold'))
trainImg.place(x=1000, y=200)

trackImg = tk.Button(window, text="Track Images", command=TrackImages, fg="white", bg="#496E7C", width=15, height=2, activebackground="white", font=('times', 15, 'bold'))
trackImg.place(x=750, y=300)

quitWindow
