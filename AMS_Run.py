import tkinter as tk
from tkinter import *
from tkinter import messagebox
import cv2
import os
import csv
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time
import pyrebase

# Initialize OpenCV face recognition modules
try:
    face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()
except Exception as e:
    print(f"Error initializing OpenCV modules: {str(e)}")

# Firebase Configuration
firebaseConfig = {
    "apiKey": "AIzaSyDhHgw1B5-gUs6FUC4bOxY4Jcal9E086eo",
    "authDomain": "YOUR_AUTH_DOMAIN",
    "projectId": "face-recognition-attenda-22db8",
    "storageBucket": "YOUR_STORAGE_BUCKET",
    "messagingSenderId": "YOUR_MESSAGING_SENDER_ID",
    "appId": "YOUR_APP_ID",
    "databaseURL": "YOUR_DATABASE_URL"
}

# Initialize Firebase
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

class LoginWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Login - Face Recognition Attendance System")
        self.window.geometry('400x400')
        self.window.configure(background='grey80')
        self.login_success = False
        
        # Email
        self.email_label = tk.Label(self.window, text="Email:", width=15, height=2, 
                                  fg="black", bg="grey", font=('times', 15, 'bold'))
        self.email_label.pack(pady=10)
        
        self.email_entry = tk.Entry(self.window, width=30)
        self.email_entry.pack(pady=5)
        
        # Password
        self.password_label = tk.Label(self.window, text="Password:", width=15, height=2,
                                     fg="black", bg="grey", font=('times', 15, 'bold'))
        self.password_label.pack(pady=10)
        
        self.password_entry = tk.Entry(self.window, width=30, show="*")
        self.password_entry.pack(pady=5)
        
        # Login Button
        self.login_button = tk.Button(self.window, text="Login", command=self.login,
                                    fg="black", bg="SkyBlue1", width=15, height=2,
                                    font=('times', 15, 'bold'))
        self.login_button.pack(pady=20)
        
        # Register Button
        self.register_button = tk.Button(self.window, text="Register", command=self.show_register,
                                       fg="black", bg="SkyBlue1", width=15, height=2,
                                       font=('times', 15, 'bold'))
        self.register_button.pack(pady=10)
        
        # Handle window close button (X)
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.window.mainloop()
    
    def on_closing(self):
        self.window.destroy()
        import sys
        sys.exit()
    
    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            messagebox.showinfo("Success", "Login Successful!")
            self.login_success = True
            self.window.destroy()
            self.show_main_window()
        except Exception as e:
            messagebox.showerror("Error", "Invalid email or password")
    
    def show_register(self):
        self.register_window = tk.Toplevel(self.window)
        self.register_window.title("Register New User")
        self.register_window.geometry('400x400')
        self.register_window.configure(background='grey80')
        
        # Handle register window close button (X)
        self.register_window.protocol("WM_DELETE_WINDOW", lambda: self.register_window.destroy())
        
        # Email
        email_label = tk.Label(self.register_window, text="Email:", width=15, height=2,
                             fg="black", bg="grey", font=('times', 15, 'bold'))
        email_label.pack(pady=10)
        
        self.reg_email_entry = tk.Entry(self.register_window, width=30)
        self.reg_email_entry.pack(pady=5)
        
        # Password
        password_label = tk.Label(self.register_window, text="Password:", width=15, height=2,
                                fg="black", bg="grey", font=('times', 15, 'bold'))
        password_label.pack(pady=10)
        
        self.reg_password_entry = tk.Entry(self.register_window, width=30, show="*")
        self.reg_password_entry.pack(pady=5)
        
        # Confirm Password
        confirm_label = tk.Label(self.register_window, text="Confirm Password:", width=15, height=2,
                               fg="black", bg="grey", font=('times', 15, 'bold'))
        confirm_label.pack(pady=10)
        
        self.reg_confirm_entry = tk.Entry(self.register_window, width=30, show="*")
        self.reg_confirm_entry.pack(pady=5)
        
        # Register Button
        register_button = tk.Button(self.register_window, text="Register", command=self.register,
                                  fg="black", bg="SkyBlue1", width=15, height=2,
                                  font=('times', 15, 'bold'))
        register_button.pack(pady=20)
    
    def register(self):
        email = self.reg_email_entry.get()
        password = self.reg_password_entry.get()
        confirm_password = self.reg_confirm_entry.get()
        
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return
        
        try:
            user = auth.create_user_with_email_and_password(email, password)
            messagebox.showinfo("Success", "Registration Successful! Please login.")
            self.register_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", "Registration failed. Please try again.")
    
    def show_main_window(self):
        # Create the main window and its components
        window = tk.Tk()
        window.title("FAMS-Face Recognition Based Attendance Management System")
        window.geometry('1280x720')
        window.configure(background='grey80')
        
        # Add all the main window components here
        # ... (rest of the main window code)

if __name__ == "__main__":
    login_window = LoginWindow()

window = tk.Tk()
window.title("FAMS-Face Recognition Based Attendance Management System")

window.geometry('1280x720')
window.configure(background='grey80')

# GUI for manually fill attendance


def manually_fill():
    global sb
    sb = tk.Tk()
    sb.title("Enter subject name...")
    sb.geometry('580x320')
    sb.configure(background='grey80')

    def err_screen_for_subject():
        def ec_delete():
            ec.destroy()
        global ec
        ec = tk.Tk()
        ec.geometry('300x100')
        ec.title('Warning!!')
        ec.configure(background='snow')
        Label(ec, text='Please enter your subject name!!!', fg='red',
              bg='white', font=('times', 16, ' bold ')).pack()
        Button(ec, text='OK', command=ec_delete, fg="black", bg="lawn green", width=9, height=1, activebackground="Red",
               font=('times', 15, ' bold ')).place(x=90, y=50)

    def fill_attendance():
        ts = time.time()
        Date = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d')
        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        Time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        Hour, Minute, Second = timeStamp.split(":")
        
        global subb
        subb = SUB_ENTRY.get()
        
        if subb == '':
            err_screen_for_subject()
        else:
            sb.destroy()
            MFW = tk.Tk()
            MFW.title("Manually attendance of " + str(subb))
            MFW.geometry('880x470')
            MFW.configure(background='grey80')

            def del_errsc2():
                errsc2.destroy()

            def err_screen1():
                global errsc2
                errsc2 = tk.Tk()
                errsc2.geometry('330x100')
                errsc2.title('Warning!!')
                errsc2.configure(background='grey80')
                Label(errsc2, text='Please enter Student & Enrollment!!!', fg='black', bg='white',
                      font=('times', 16, ' bold ')).pack()
                Button(errsc2, text='OK', command=del_errsc2, fg="black", bg="lawn green", width=9, height=1,
                       activebackground="Red", font=('times', 15, ' bold ')).place(x=90, y=50)

            def testVal(inStr, acttyp):
                if acttyp == '1':  # insert
                    if not inStr.isdigit():
                        return False
                return True

            ENR = tk.Label(MFW, text="Enter Enrollment", width=15, height=2, fg="black", bg="grey",
                          font=('times', 15))
            ENR.place(x=30, y=100)

            STU_NAME = tk.Label(MFW, text="Enter Student name", width=15, height=2, fg="black", bg="grey",
                              font=('times', 15))
            STU_NAME.place(x=30, y=200)

            global ENR_ENTRY
            ENR_ENTRY = tk.Entry(MFW, width=20, validate='key',
                               bg="white", fg="black", font=('times', 23))
            ENR_ENTRY['validatecommand'] = (
                ENR_ENTRY.register(testVal), '%P', '%d')
            ENR_ENTRY.place(x=290, y=105)

            def remove_enr():
                ENR_ENTRY.delete(first=0, last=22)

            STUDENT_ENTRY = tk.Entry(
                MFW, width=20, bg="white", fg="black", font=('times', 23))
            STUDENT_ENTRY.place(x=290, y=205)

            def remove_student():
                STUDENT_ENTRY.delete(first=0, last=22)

            def enter_data_DB():
                ENROLLMENT = ENR_ENTRY.get()
                STUDENT = STUDENT_ENTRY.get()
                if ENROLLMENT == '':
                    err_screen1()
                elif STUDENT == '':
                    err_screen1()
                else:
                    try:
                        # Get the base directory of the script
                        base_dir = os.path.dirname(os.path.abspath(__file__))
                        
                        # Create directory path relative to script location
                        attendance_dir = os.path.join(base_dir, 'Attendance', 'Manually Attendance')
                        
                        # Create directory with parents if it doesn't exist
                        os.makedirs(attendance_dir, exist_ok=True)
                        
                        ts = time.time()
                        date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                        Hour, Minute, Second = timeStamp.split(":")
                        
                        # Create CSV file name and path
                        file_name = f"{subb}_{date}_Time_{Hour}_{Minute}_{Second}.csv"
                        attendance_path = os.path.join(attendance_dir, file_name)
                        
                        # Check if file exists, create with headers if it doesn't
                        if not os.path.exists(attendance_path):
                            with open(attendance_path, 'w', newline='') as csvFile:
                                writer = csv.writer(csvFile)
                                writer.writerow(['ID', 'ENROLLMENT', 'NAME', 'DATE', 'TIME'])
                        
                        # Append the attendance record
                        with open(attendance_path, 'a+', newline='') as csvFile:
                            writer = csv.writer(csvFile)
                            row_count = sum(1 for row in csv.reader(open(attendance_path)))
                            writer.writerow([row_count, ENROLLMENT, STUDENT, date, timeStamp])
                        
                        ENR_ENTRY.delete(first=0, last=22)
                        STUDENT_ENTRY.delete(first=0, last=22)
                        
                        # Show success notification
                        Notifi.configure(text="Attendance saved successfully", bg="Green", fg="white",
                                       width=33, font=('times', 19, 'bold'))
                        Notifi.place(x=180, y=380)
                        
                    except PermissionError as pe:
                        error_msg = "Permission denied: Unable to create directory or save file. Please run as administrator or check folder permissions."
                        print(f"Permission error: {str(pe)}")
                        Notifi.configure(text=error_msg, bg="red", fg="white",
                                       width=33, font=('times', 19, 'bold'))
                        Notifi.place(x=180, y=380)
                    except Exception as e:
                        error_msg = f"Error saving attendance: {str(e)}"
                        print(f"Error: {error_msg}")
                        Notifi.configure(text=error_msg, bg="red", fg="white",
                                       width=33, font=('times', 19, 'bold'))
                        Notifi.place(x=180, y=380)

            def create_csv():
                try:
                    # Get the base directory of the script
                    base_dir = os.path.dirname(os.path.abspath(__file__))
                    attendance_dir = os.path.join(base_dir, 'Attendance', 'Manually Attendance')
                    file_name = f"{subb}_{Date}_Time_{Hour}_{Minute}_{Second}.csv"
                    csv_name = os.path.join(attendance_dir, file_name)
                    
                    if os.path.exists(csv_name):
                        # Display the attendance data
                        root = tk.Tk()
                        root.title(f"Attendance of {subb}")
                        root.configure(background='grey80')
                        
                        with open(csv_name, newline="") as file:
                            reader = csv.reader(file)
                            r = 0
                            for col in reader:
                                c = 0
                                for row in col:
                                    label = tk.Label(root, width=18, height=1, fg="black", 
                                                   font=('times', 13, ' bold '),
                                                   bg="white", text=row, relief=tk.RIDGE)
                                    label.grid(row=r, column=c)
                                    c += 1
                                r += 1
                        root.mainloop()
                        
                        O = "CSV created Successfully"
                        Notifi.configure(text=O, bg="Green", fg="white",
                                       width=33, font=('times', 19, 'bold'))
                        Notifi.place(x=180, y=380)
                    else:
                        O = "No attendance records found"
                        Notifi.configure(text=O, bg="red", fg="white",
                                       width=33, font=('times', 19, 'bold'))
                        Notifi.place(x=180, y=380)
                except Exception as es:
                    print(f"Error: {str(es)}")
                    Notifi.configure(text="Error creating CSV", bg="red", fg="white",
                                   width=33, font=('times', 19, 'bold'))
                    Notifi.place(x=180, y=380)

            Notifi = tk.Label(MFW, text="CSV created Successfully", bg="Green", fg="white", width=33,
                            height=2, font=('times', 19, 'bold'))

            c1ear_enroll = tk.Button(MFW, text="Clear", command=remove_enr, fg="white", bg="black",
                                   width=10, height=1,
                                   activebackground="white", font=('times', 15, ' bold '))
            c1ear_enroll.place(x=690, y=100)

            c1ear_student = tk.Button(MFW, text="Clear", command=remove_student, fg="white", bg="black",
                                    width=10, height=1,
                                    activebackground="white", font=('times', 15, ' bold '))
            c1ear_student.place(x=690, y=200)

            DATA_SUB = tk.Button(MFW, text="Enter Data", command=enter_data_DB, fg="black", bg="SkyBlue1",
                               width=20, height=2,
                               activebackground="white", font=('times', 15, ' bold '))
            DATA_SUB.place(x=170, y=300)

            MAKE_CSV = tk.Button(MFW, text="Show Attendance", command=create_csv, fg="black", bg="SkyBlue1",
                               width=20, height=2,
                               activebackground="white", font=('times', 15, ' bold '))
            MAKE_CSV.place(x=570, y=300)

            def attf():
                import subprocess
                subprocess.Popen(r'explorer "' + os.path.abspath("Attendance/Manually Attendance") + '"')

            attf = tk.Button(MFW, text="Check Sheets", command=attf, fg="white", bg="black",
                           width=12, height=1, activebackground="white", font=('times', 14, ' bold '))
            attf.place(x=730, y=410)

            MFW.mainloop()

    SUB = tk.Label(sb, text="Enter Subject : ", width=15, height=2,
                  fg="black", bg="grey80", font=('times', 15, ' bold '))
    SUB.place(x=30, y=100)

    global SUB_ENTRY
    SUB_ENTRY = tk.Entry(sb, width=20, bg="white",
                        fg="black", font=('times', 23))
    SUB_ENTRY.place(x=250, y=105)

    fill_manual_attendance = tk.Button(sb, text="Fill Attendance", command=fill_attendance, fg="black", bg="SkyBlue1", width=20, height=2,
                                     activebackground="white", font=('times', 15, ' bold '))
    fill_manual_attendance.place(x=250, y=160)
    sb.mainloop()

# For clear textbox


def clear():
    txt.delete(first=0, last=22)


def clear1():
    txt2.delete(first=0, last=22)


def del_sc1():
    sc1.destroy()


def err_screen():
    global sc1
    sc1 = tk.Tk()
    sc1.geometry('300x100')
    sc1.title('Warning!!')
    sc1.configure(background='grey80')
    Label(sc1, text='Enrollment & Name required!!!', fg='black',
          bg='white', font=('times', 16)).pack()
    Button(sc1, text='OK', command=del_sc1, fg="black", bg="lawn green", width=9,
           height=1, activebackground="Red", font=('times', 15, ' bold ')).place(x=90, y=50)

# Error screen2


def del_sc2():
    sc2.destroy()


def err_screen1():
    global sc2
    sc2 = tk.Tk()
    sc2.geometry('300x100')
    sc2.title('Warning!!')
    sc2.configure(background='grey80')
    Label(sc2, text='Please enter your subject name!!!', fg='black',
          bg='white', font=('times', 16)).pack()
    Button(sc2, text='OK', command=del_sc2, fg="black", bg="lawn green", width=9,
           height=1, activebackground="Red", font=('times', 15, ' bold ')).place(x=90, y=50)

# For take images for datasets


def take_img():
    l1 = txt.get()
    l2 = txt2.get()
    if l1 == '':
        err_screen()
    elif l2 == '':
        err_screen()
    else:
        try:
            # Create required directories if they don't exist
            base_dir = os.path.dirname(os.path.abspath(__file__))
            required_dirs = {
                'StudentDetails': os.path.join(base_dir, 'StudentDetails'),
                'TrainingImage': os.path.join(base_dir, 'TrainingImage'),
                'TrainingImageLabel': os.path.join(base_dir, 'TrainingImageLabel')
            }
            
            for dir_name, dir_path in required_dirs.items():
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)
                    print(f"Created directory: {dir_path}")

            # Initialize camera
            cam = cv2.VideoCapture(0)
            if not cam.isOpened():
                raise Exception("Unable to access webcam")

            # Initialize face detector
            detector = cv2.CascadeClassifier(os.path.join(base_dir, 'haarcascade_frontalface_default.xml'))
            if detector.empty():
                raise Exception("Failed to load face detector cascade")

            Enrollment = txt.get()
            Name = txt2.get()
            sampleNum = 0
            
            # Display a message to user
            progress_label = tk.Label(window, text="Capturing images... Please look at the camera.", 
                                    bg="yellow", fg="black", font=('times', 15, 'bold'))
            progress_label.place(x=350, y=400)
            window.update()

            while sampleNum < 70:  # Taking 70 samples
                ret, img = cam.read()
                if not ret:
                    raise Exception("Failed to capture frame from camera")
                    
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                
                for (x, y, w, h) in faces:
                    sampleNum = sampleNum + 1
                    # saving the captured face in the dataset folder
                    img_name = os.path.join(required_dirs['TrainingImage'], f"{Name}.{Enrollment}.{sampleNum}.jpg")
                    cv2.imwrite(img_name, gray[y:y + h, x:x + w])
                    
                    # Draw rectangle around detected face
                    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    
                    # Update progress message
                    progress_label.config(text=f"Capturing image {sampleNum}/70... Please look at the camera.")
                    window.update()
                    
                    # Display the image
                    cv2.imshow('Capturing Face Samples', img)
                    
                # Add a small delay between captures
                cv2.waitKey(100)

            cam.release()
            cv2.destroyAllWindows()
            progress_label.destroy()

            # Save student details to CSV
            ts = time.time()
            Date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            Time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            
            # Use the path from required_dirs
            csv_file_path = os.path.join(required_dirs['StudentDetails'], 'StudentDetails.csv')
            
            # Create CSV file if it doesn't exist
            if not os.path.exists(csv_file_path):
                with open(csv_file_path, 'w', newline='') as csvFile:
                    writer = csv.writer(csvFile)
                    writer.writerow(['Enrollment', 'Name', 'Date', 'Time'])
            
            # Append the new record
            row = [Enrollment, Name, Date, Time]
            with open(csv_file_path, 'a+', newline='') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(row)
                
            # Show success message
            res = f"Images Saved for Enrollment: {Enrollment}, Name: {Name}"
            Notification.configure(text=res, bg="SpringGreen3", width=50, font=('times', 18, 'bold'))
            Notification.place(x=250, y=400)
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            print(f"Error during image capture: {error_msg}")
            if 'cam' in locals():
                cam.release()
            cv2.destroyAllWindows()
            if 'progress_label' in locals():
                progress_label.destroy()
            Notification.configure(text=error_msg, bg="red", width=50, font=('times', 18, 'bold'))
            Notification.place(x=250, y=400)


# for choose subject and fill attendance
def subjectchoose():
    def Fillattendances():
        sub = tx.get()
        now = time.time()
        future = now + 20
        
        if time.time() < future:
            if sub == '':
                err_screen1()
            else:
                try:
                    # Create necessary directories if they don't exist
                    current_dir = os.path.dirname(os.path.abspath(__file__))
                    attendance_dir = os.path.join(current_dir, "Attendance")
                    training_label_dir = os.path.join(current_dir, "TrainingImageLabel")
                    
                    for directory in [attendance_dir, training_label_dir]:
                        if not os.path.exists(directory):
                            os.makedirs(directory)
                            print(f"Created directory: {directory}")
                    
                    # Set up model and cascade paths
                    model_path = os.path.join(training_label_dir, "Trainner.yml")
                    haarcascade_path = os.path.join(current_dir, "haarcascade_frontalface_default.xml")
                    
                    print(f"Looking for model at: {model_path}")
                    print(f"Using cascade at: {haarcascade_path}")
                    
                    # Verify model exists
                    if not os.path.exists(model_path):
                        error_msg = f"Model not found at {model_path}. Please train the model first."
                        print(error_msg)
                        Notifica.configure(text=error_msg, bg="red", fg="black",
                                        width=33, font=('times', 15, 'bold'))
                        Notifica.place(x=20, y=250)
                        return
                        
                    # Initialize face recognition
                    recognizer = cv2.face.LBPHFaceRecognizer_create()
                    recognizer.read(model_path)
                    
                    # Initialize face detector
                    detector = cv2.CascadeClassifier(haarcascade_path)
                    if detector.empty():
                        error_msg = "Failed to load face detector"
                        print(error_msg)
                        Notifica.configure(text=error_msg, bg="red", fg="black",
                                        width=33, font=('times', 15, 'bold'))
                        Notifica.place(x=20, y=250)
                        return
                    
                    # Load student details
                    student_details_path = os.path.join(current_dir, "StudentDetails", "StudentDetails.csv")
                    if not os.path.exists(student_details_path):
                        error_msg = "Student details file not found"
                        print(error_msg)
                        Notifica.configure(text=error_msg, bg="red", fg="black",
                                        width=33, font=('times', 15, 'bold'))
                        Notifica.place(x=20, y=250)
                        return
                        
                    df = pd.read_csv(student_details_path)
                    
                    # Initialize camera
                    cam = cv2.VideoCapture(0)
                    if not cam.isOpened():
                        error_msg = "Failed to open camera"
                        print(error_msg)
                        Notifica.configure(text=error_msg, bg="red", fg="black",
                                        width=33, font=('times', 15, 'bold'))
                        Notifica.place(x=20, y=250)
                        return
                    
                    # Initialize attendance tracking
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    col_names = ['Enrollment', 'Name', 'Date', 'Time']
                    attendance = pd.DataFrame(columns=col_names)
                    
                    print("Starting face recognition...")
                    
                    # Main recognition loop
                    while True:
                        ret, im = cam.read()
                        if not ret:
                            print("Failed to grab frame")
                            break
                            
                        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                        faces = detector.detectMultiScale(gray, 1.2, 5)
                        
                        for (x, y, w, h) in faces:
                            try:
                                Id, conf = recognizer.predict(gray[y:y + h, x:x + w])
                                if conf < 70:
                                    ts = time.time()
                                    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                                    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                                    aa = df.loc[df['Enrollment'] == Id]['Name'].values
                                    tt = str(Id) + "-" + str(aa)
                                    attendance.loc[len(attendance)] = [Id, aa, date, timeStamp]
                                    
                                    cv2.rectangle(im, (x, y), (x + w, y + h), (0, 260, 0), 7)
                                    cv2.putText(im, str(tt), (x + h, y), font, 1, (255, 255, 0,), 4)
                                else:
                                    Id = 'Unknown'
                                    tt = str(Id)
                                    cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 7)
                                    cv2.putText(im, str(tt), (x + h, y), font, 1, (0, 25, 255), 4)
                            except Exception as e:
                                print(f"Error processing face: {str(e)}")
                                continue
                        
                        attendance = attendance.drop_duplicates(['Enrollment'], keep='first')
                        cv2.imshow('Taking Attendance', im)
                        
                        if cv2.waitKey(1) == 27 or time.time() > future:
                            break
                    
                    # Clean up camera
                    cam.release()
                    cv2.destroyAllWindows()
                    
                    # Save attendance
                    if not attendance.empty:
                        ts = time.time()
                        date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                        Hour, Minute, Second = timeStamp.split(":")
                        
                        fileName = os.path.join(attendance_dir, 
                                              f"{sub}_{date}_{Hour}-{Minute}-{Second}.csv")
                        
                        attendance.to_csv(fileName, index=False)
                        print(f"Saved attendance to {fileName}")
                        
                        # Show success message
                        Notifica.configure(text="Attendance saved successfully", 
                                        bg="green", fg="white",
                                        width=33, font=('times', 15, 'bold'))
                        Notifica.place(x=20, y=250)
                        
                        # Display attendance
                        root = tk.Tk()
                        root.title(f"Attendance of {sub}")
                        root.configure(background='grey80')
                        
                        with open(fileName, newline="") as file:
                            reader = csv.reader(file)
                            r = 0
                            for col in reader:
                                c = 0
                                for row in col:
                                    label = tk.Label(root, width=10, height=1, 
                                                   fg="black", 
                                                   font=('times', 15, 'bold'),
                                                   bg="white", text=row, 
                                                   relief=tk.RIDGE)
                                    label.grid(row=r, column=c)
                                    c += 1
                                r += 1
                        root.mainloop()
                    else:
                        print("No attendance records to save")
                        Notifica.configure(text="No attendance records to save", 
                                        bg="red", fg="white",
                                        width=33, font=('times', 15, 'bold'))
                        Notifica.place(x=20, y=250)
                        
                except Exception as e:
                    error_msg = f"Error: {str(e)}"
                    print(error_msg)
                    Notifica.configure(text=error_msg, bg="red", fg="black",
                                    width=33, font=('times', 15, 'bold'))
                    Notifica.place(x=20, y=250)

    # windo is frame for subject chooser
    windo = tk.Tk()
    windo.title("Enter subject name...")
    windo.geometry('580x320')
    windo.configure(background='grey80')
    Notifica = tk.Label(windo, text="Attendance filled Successfully", bg="Green", fg="white", width=33,
                        height=2, font=('times', 15, 'bold'))

    def Attf():
        import subprocess
        subprocess.Popen(
            r'explorer \select,"C:\Users\Artee\Downloads\Face-Recognition-Attendance-System-main\Face-Recognition-Attendance-System-main\Attendance\-------Check atttendance-------"')

    attf = tk.Button(windo,  text="Check Sheets", command=Attf, fg="white", bg="black",
                     width=12, height=1, activebackground="white", font=('times', 14, ' bold '))
    attf.place(x=430, y=255)

    sub = tk.Label(windo, text="Enter Subject : ", width=15, height=2,
                   fg="black", bg="grey", font=('times', 15, ' bold '))
    sub.place(x=30, y=100)

    tx = tk.Entry(windo, width=20, bg="white",
                  fg="black", font=('times', 23))
    tx.place(x=250, y=105)

    fill_a = tk.Button(windo, text="Fill Attendance", fg="white", command=Fillattendances, bg="SkyBlue1", width=20, height=2,
                       activebackground="white", font=('times', 15, ' bold '))
    fill_a.place(x=250, y=160)
    windo.mainloop()


def admin_panel():
    win = tk.Tk()
    win.title("LogIn")
    win.geometry('880x420')
    win.configure(background='grey80')

    def log_in():
        username = un_entr.get()
        password = pw_entr.get()

        if username == 'rahul':
            if password == 'rahul':
                win.destroy()
                import csv
                import tkinter
                root = tkinter.Tk()
                root.title("Student Details")
                root.configure(background='grey80')

                cs = 'C:/Users/Artee/Downloads/Face-Recognition-Attendance-System-main/Face-Recognition-Attendance-System-main/StudentDetails/StudentDetails.csv'
                with open(cs, newline="") as file:
                    reader = csv.reader(file)
                    r = 0

                    for col in reader:
                        c = 0
                        for row in col:
                            # i've added some styling
                            label = tkinter.Label(root, width=10, height=1, fg="black", font=('times', 15, ' bold '),
                                                  bg="white", text=row, relief=tkinter.RIDGE)
                            label.grid(row=r, column=c)
                            c += 1
                        r += 1
                root.mainloop()
            else:
                valid = 'Incorrect ID or Password'
                Nt.configure(text=valid, bg="red", fg="white",
                             width=38, font=('times', 19, 'bold'))
                Nt.place(x=120, y=350)

        else:
            valid = 'Incorrect ID or Password'
            Nt.configure(text=valid, bg="red", fg="white",
                         width=38, font=('times', 19, 'bold'))
            Nt.place(x=120, y=350)

    Nt = tk.Label(win, text="Attendance filled Successfully", bg="Green", fg="white", width=40,
                  height=2, font=('times', 19, 'bold'))

    un = tk.Label(win, text="Enter username : ", width=15, height=2, fg="black", bg="grey",
                  font=('times', 15, ' bold '))
    un.place(x=30, y=50)

    pw = tk.Label(win, text="Enter password : ", width=15, height=2, fg="black", bg="grey",
                  font=('times', 15, ' bold '))
    pw.place(x=30, y=150)

    def c00():
        un_entr.delete(first=0, last=22)

    un_entr = tk.Entry(win, width=20, bg="white", fg="black",
                       font=('times', 23))
    un_entr.place(x=290, y=55)

    def c11():
        pw_entr.delete(first=0, last=22)

    pw_entr = tk.Entry(win, width=20, show="*", bg="white",
                       fg="black", font=('times', 23))
    pw_entr.place(x=290, y=155)

    c0 = tk.Button(win, text="Clear", command=c00, fg="white", bg="black", width=10, height=1,
                   activebackground="white", font=('times', 15, ' bold '))
    c0.place(x=690, y=55)

    c1 = tk.Button(win, text="Clear", command=c11, fg="white", bg="black", width=10, height=1,
                   activebackground="white", font=('times', 15, ' bold '))
    c1.place(x=690, y=155)

    Login = tk.Button(win, text="LogIn", fg="black", bg="SkyBlue1", width=20,
                      height=2,
                      activebackground="Red", command=log_in, font=('times', 15, ' bold '))
    Login.place(x=290, y=250)
    win.mainloop()


# For train the model
def trainimg():
    try:
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        
        # Get absolute paths
        current_dir = os.path.dirname(os.path.abspath(__file__))
        haarcascade_path = os.path.join(current_dir, "haarcascade_frontalface_default.xml")
        training_image_path = os.path.join(current_dir, "TrainingImage")
        training_label_path = os.path.join(current_dir, "TrainingImageLabel")
        model_path = os.path.join(training_label_path, "Trainner.yml")
        
        print(f"Starting training process...")
        print(f"Current directory: {current_dir}")
        print(f"Training image path: {training_image_path}")
        print(f"Model will be saved to: {model_path}")
        
        # Ensure TrainingImageLabel directory exists
        if not os.path.exists(training_label_path):
            os.makedirs(training_label_path)
            print(f"Created TrainingImageLabel directory")
        
        # Check for training images
        if not os.path.exists(training_image_path):
            error_msg = "Training Image folder is missing"
            print(error_msg)
            Notification.configure(text=error_msg, bg="red", fg="white",
                                width=50, font=('times', 18, 'bold'))
            Notification.place(x=250, y=400)
            return

        image_files = [f for f in os.listdir(training_image_path) if f.endswith('.jpg')]
        if not image_files:
            error_msg = "No training images found"
            print(error_msg)
            Notification.configure(text=error_msg, bg="red", fg="white",
                                width=50, font=('times', 18, 'bold'))
            Notification.place(x=250, y=400)
            return
            
        print(f"Found {len(image_files)} training images")
        
        # Initialize face detector
        detector = cv2.CascadeClassifier(haarcascade_path)
        if detector.empty():
            error_msg = "Failed to load face detector"
            print(error_msg)
            Notification.configure(text=error_msg, bg="red", fg="white",
                                width=50, font=('times', 18, 'bold'))
            Notification.place(x=250, y=400)
            return

        # Prepare training data
        faces = []
        ids = []
        
        for img_name in image_files:
            try:
                img_path = os.path.join(training_image_path, img_name)
                print(f"Processing {img_path}")
                
                # Load and convert image
                PIL_img = Image.open(img_path).convert('L')
                img_numpy = np.array(PIL_img, 'uint8')
                
                # Extract ID from filename (format: name.id.number.jpg)
                id = int(img_name.split('.')[1])
                
                # Detect face
                detected_faces = detector.detectMultiScale(img_numpy)
                
                if len(detected_faces) == 0:
                    print(f"No face detected in {img_name}")
                    continue
                    
                for (x, y, w, h) in detected_faces:
                    faces.append(img_numpy[y:y+h, x:x+w])
                    ids.append(id)
                    
            except Exception as e:
                print(f"Error processing {img_name}: {str(e)}")
                continue

        if not faces:
            error_msg = "No faces could be detected in training images"
            print(error_msg)
            Notification.configure(text=error_msg, bg="red", fg="white",
                                width=50, font=('times', 18, 'bold'))
            Notification.place(x=250, y=400)
            return
            
        print(f"Successfully processed {len(faces)} faces")
        
        # Train the model
        print("Training model...")
        recognizer.train(faces, np.array(ids))
        
        # Save the model
        print(f"Saving model to {model_path}")
        recognizer.write(model_path)
        
        # Verify the model was saved
        if os.path.exists(model_path):
            success_msg = f"Model trained successfully! ({len(faces)} faces)"
            print(success_msg)
            Notification.configure(text=success_msg, bg="SpringGreen3", fg="white",
                                width=50, font=('times', 18, 'bold'))
            Notification.place(x=250, y=400)
        else:
            error_msg = "Failed to save model file"
            print(error_msg)
            Notification.configure(text=error_msg, bg="red", fg="white",
                                width=50, font=('times', 18, 'bold'))
            Notification.place(x=250, y=400)
            
    except Exception as e:
        error_msg = f"Training error: {str(e)}"
        print(error_msg)
        Notification.configure(text=error_msg, bg="red", fg="white",
                            width=50, font=('times', 18, 'bold'))
        Notification.place(x=250, y=400)


window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)


def on_closing():
    from tkinter import messagebox
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        window.destroy()


window.protocol("WM_DELETE_WINDOW", on_closing)

message = tk.Label(window, text="Face-Recognition-Based-Attendance-Management-System", bg="black", fg="white", width=50,
                   height=3, font=('times', 30, ' bold '))

message.place(x=80, y=20)

Notification = tk.Label(window, text="All things good", bg="Green", fg="white", width=15,
                        height=3, font=('times', 17))

lbl = tk.Label(window, text="Enter Enrollment : ", width=20, height=2,
               fg="black", bg="grey", font=('times', 15, 'bold'))
lbl.place(x=200, y=200)


def testVal(inStr, acttyp):
    if acttyp == '1':  # insert
        if not inStr.isdigit():
            return False
    return True


txt = tk.Entry(window, validate="key", width=20, bg="white",
               fg="black", font=('times', 25))
txt['validatecommand'] = (txt.register(testVal), '%P', '%d')
txt.place(x=550, y=210)

lbl2 = tk.Label(window, text="Enter Name : ", width=20, fg="black",
                bg="grey", height=2, font=('times', 15, ' bold '))
lbl2.place(x=200, y=300)

txt2 = tk.Entry(window, width=20, bg="white",
                fg="black", font=('times', 25))
txt2.place(x=550, y=310)

clearButton = tk.Button(window, text="Clear", command=clear, fg="white", bg="black",
                        width=10, height=1, activebackground="white", font=('times', 15, ' bold '))
clearButton.place(x=950, y=210)

clearButton1 = tk.Button(window, text="Clear", command=clear1, fg="white", bg="black",
                         width=10, height=1, activebackground="white", font=('times', 15, ' bold '))
clearButton1.place(x=950, y=310)

AP = tk.Button(window, text="Check Registered students", command=admin_panel, fg="black",
               bg="SkyBlue1", width=19, height=1, activebackground="white", font=('times', 15, ' bold '))
AP.place(x=990, y=410)

takeImg = tk.Button(window, text="Take Images", command=take_img, fg="black", bg="SkyBlue1",
                    width=20, height=3, activebackground="white", font=('times', 15, ' bold '))
takeImg.place(x=90, y=500)

trainImg = tk.Button(window, text="Train Images", fg="black", command=trainimg, bg="SkyBlue1",
                     width=20, height=3, activebackground="white", font=('times', 15, ' bold '))
trainImg.place(x=390, y=500)

FA = tk.Button(window, text="Automatic Attendance", fg="black", command=subjectchoose,
               bg="SkyBlue1", width=20, height=3, activebackground="white", font=('times', 15, ' bold '))
FA.place(x=690, y=500)

quitWindow = tk.Button(window, text="Manually Fill Attendance", command=manually_fill, fg="black",
                       bg="SkyBlue1", width=20, height=3, activebackground="white", font=('times', 15, ' bold '))
quitWindow.place(x=990, y=500)

window.mainloop()
