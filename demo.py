import tkinter as tk
import cv2
import csv
import os
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time

# Window is our Main frame of the system
window = tk.Tk()
window.title("FAMS-Face Recognition Based Attendance Management System")
window.geometry('1280x720')
window.configure(background='black')

# GUI for manually fill attendance
def manually_fill():
    global sb
    sb = tk.Tk()
    sb.title("Enter subject name...")
    sb.geometry('580x320')
    sb.configure(background='black')

    def err_screen_for_subject():
        global ec
        ec = tk.Tk()
        ec.geometry('300x100')
        ec.title('Warning!!')
        ec.configure(background='snow')
        Label(ec, text='Please enter your subject name!!!', fg='red',
              bg='white', font=('times', 16, ' bold ')).pack()
        Button(ec, text='OK', command=ec.destroy, fg="white", bg="lawn green", width=9, height=1,
               activebackground="Red", font=('times', 15, ' bold ')).place(x=90, y=50)

    def fill_attendance():
        ts = time.time()
        Date = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d')
        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        Time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        Hour, Minute, Second = timeStamp.split(":")
        # Creating csv of attendance

        # Create a table for Attendance
        date_for_DB = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d')
        global subb
        subb = SUB_ENTRY.get()
        DB_table_name = str(subb + "_" + Date + "_Time_" +
                            Hour + "_" + Minute + "_" + Second)

        import pymysql.connections

        # Connect to the database
        try:
            global cursor
            connection = pymysql.connect(
                host='localhost', user='root', password='root', db="manually_fill_attendance")
            cursor = connection.cursor()
        except Exception as e:
            print(e)

        sql = "CREATE TABLE " + DB_table_name + """
                        (ID INT NOT NULL AUTO_INCREMENT,
                         ENROLLMENT varchar(100) NOT NULL,
                         NAME VARCHAR(50) NOT NULL,
                         DATE VARCHAR(20) NOT NULL,
                         TIME VARCHAR(20) NOT NULL,
                             PRIMARY KEY (ID)
                             );
                        """

        try:
            cursor.execute(sql)  # for create a table
        except Exception as ex:
            print(ex)

        if subb == '':
            err_screen_for_subject()
        else:
            sb.destroy()
            MFW = tk.Tk()
            MFW.title("Manually attendance of " + str(subb))
            MFW.geometry('880x470')
            MFW.configure(background='black')

            def del_errsc2():
                errsc2.destroy()

            def err_screen1():
                global errsc2
                errsc2 = tk.Tk()
                errsc2.geometry('330x100')
                errsc2.title('Warning!!')
                errsc2.configure(background='black')
                Label(errsc2, text='Please enter Student & Enrollment!!!', fg='black', bg='white',
                      font=('times', 16, ' bold ')).pack()
                Button(errsc2, text='OK', command=del_errsc2, fg="white", bg="lawn green", width=9, height=1,
                       activebackground="Red", font=('times', 15, ' bold ')).place(x=90, y=50)

            def testVal(inStr, acttyp):
                if acttyp == '1':  # insert
                    if not inStr.isdigit():
                        return False
                return True

            ENR = tk.Label(MFW, text="Enter Enrollment", width=15, height=2, fg="white", bg="black",
                           font=('times', 15))
            ENR.place(x=30, y=100)

            STU_NAME = tk.Label(MFW, text="Enter Student name", width=15, height=2, fg="white", bg="black",
                                font=('times', 15))
            STU_NAME.place(x=30, y=200)

            global ENR_ENTRY
            ENR_ENTRY = tk.Entry(MFW, width=20, validate='key',
                                 bg="black", fg="white", font=('times', 23))
            ENR_ENTRY['validatecommand'] = (
                ENR_ENTRY.register(testVal), '%P', '%d')
            ENR_ENTRY.place(x=290, y=105)

            def remove_enr():
                ENR_ENTRY.delete(first=0, last=22)

            STUDENT_ENTRY = tk.Entry(
                MFW, width=20, bg="black", fg="white", font=('times', 23))
            STUDENT_ENTRY.place(x=290, y=205)

            def remove_student():
                STUDENT_ENTRY.delete(first=0, last=22)

            # get important variable
            def enter_data_DB():
                ENROLLMENT = ENR_ENTRY.get()
                STUDENT = STUDENT_ENTRY.get()
                if ENROLLMENT == '' and STUDENT == '':
                    err_screen1()
                else:
                    time = datetime.datetime.fromtimestamp(
                        ts).strftime('%H:%M:%S')
                    Hour, Minute, Second = time.split(":")
                    Insert_data = "INSERT INTO " + DB_table_name + " (ID,ENROLLMENT,NAME,DATE,TIME) VALUES (0, %s, %s, %s,%s)"
                    VALUES = (str(ENROLLMENT), str(STUDENT), str(Date), str(time))
                    try:
                        cursor.execute(Insert_data, VALUES)
                    except Exception as e:
                        print(e)
                    ENR_ENTRY.delete(first=0, last=22)
                    STUDENT_ENTRY.delete(first=0, last=22)

            def create_csv():
                import csv
                cursor.execute("select * from " + DB_table_name + ";")
                # fetch all the records
                rows = cursor.fetchall()
                # write data in CSV file
                with open("Manually Attendance Sheet of" + subb + ".csv", "w") as csvfile:
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow(['ID', 'ENROLLMENT', 'NAME', 'DATE', 'TIME'])
                    csvwriter.writerows(rows)

                MFW.destroy()

            print(os.getcwd())
            attf = os.path.join(os.getcwd(), "Manually Attendance of" + subb + ".csv")
            print(attf)
            attf2 = attf.replace("\\", "/")
            print(attf2)

            cdb = tk.Button(MFW, text="Create CSV", fg="white", bg="blue", width=15,
                            height=2, activebackground="Red", font=('times', 15, ' bold '), command=create_csv)
            cdb.place(x=550, y=380)

            # cdb = tk.Button(MFW, text="Create DB", fg="white", bg="green", width=10,
            #                 height=2, activebackground="Red", font=('times', 15, ' bold '), command=create_db)
            # cdb.place(x=590, y=380)

            # cdb = tk.Button(MFW, text="Create Both", fg="white", bg="magenta", width=10,
            #                 height=2, activebackground="Red", font=('times', 15, ' bold '), command=create_db_and_csv)
            # cdb.place(x=720, y=380)

            sch = tk.Button(MFW, text="ENTER DATA", fg="black", bg="lawn green", width=15,
                            height=2, activebackground="Red", font=('times', 15, ' bold '), command=enter_data_DB)
            sch.place(x=30, y=380)

            def del_errsc1():
                errsc1.destroy()

            def err_screen():
                global errsc1
                errsc1 = tk.Tk()
                errsc1.geometry('330x100')
                errsc1.title('Warning!!')
                errsc1.configure(background='black')
                Label(errsc1, text='Please enter subject name!!!', fg='black', bg='white',
                      font=('times', 16, ' bold ')).pack()
                Button(errsc1, text='OK', command=del_errsc1, fg="white", bg="lawn green", width=9, height=1,
                       activebackground="Red", font=('times', 15, ' bold ')).place(x=90, y=50)

            def enter_data():
                ts = time.time()
                Date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                Time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                Hour, Minute, Second = timeStamp.split(":")
                try:
                    if subject == '':
                        err_screen()
                    else:
                        # Create a table for Attendance
                        date_for_DB = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d')
                        global subb
                        subb = subject.replace(" ", "_") + "_" + Date + "_Time_" + Hour + "_" + Minute + "_" + Second
                        import pymysql.connections

                        # Connect to the database
                        try:
                            global cursor
                            connection = pymysql.connect(
                                host='localhost', user='root', password='root', db="Manually_fill_attendance")
                            cursor = connection.cursor()
                        except Exception as e:
                            print(e)

                        sql = "CREATE TABLE " + subb + """
                                (ID INT NOT NULL AUTO_INCREMENT,
                                 ENROLLMENT varchar(100) NOT NULL,
                                 NAME VARCHAR(50) NOT NULL,
                                 DATE VARCHAR(20) NOT NULL,
                                 TIME VARCHAR(20) NOT NULL,
                                 PRIMARY KEY (ID)
                                 );
                                """

                        try:
                            cursor.execute(sql)  # for create a table
                        except Exception as ex:
                            print(ex)

                        message.configure(text=subb + " Attendance filled Successfully!!!")
                        print(subb + "Attendance Filled Successfully")

                except Exception as e:
                    print(e)

            subject = SUB_ENTRY.get()
            ts = time.time()
            Date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            Time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            Hour, Minute, Second = timeStamp.split(":")

            DATE_TIME = Date + " " + Hour + ":" + Minute + ":" + Second

            # creating the database if not exists named attendance
            import pymysql.connections

            try:
                connection = pymysql.connect(
                    host='localhost', user='root', password='root')
                cursor = connection.cursor()
                # execute the SQL query to create a database
                cursor.execute("CREATE DATABASE if not exists attendance")
                # commit the changes
                connection.commit()
                connection.close()
            except Exception as e:
                print(e)

            try:
                connection = pymysql.connect(
                    host='localhost', user='root', password='root', db="attendance")
                cursor = connection.cursor()
                # execute the SQL query to create a table in the database
                cursor.execute(
                    "CREATE TABLE if not exists record (NAME varchar(100),DATE varchar(50),TIME varchar(50))")
                # commit the changes
                connection.commit()
                # close the connection
                connection.close()
            except Exception as e:
                print(e)

            # check if the table exists or not, if not then create the table
            connection = pymysql.connect(
                host='localhost', user='root', password='root', db="attendance")
            cursor = connection.cursor()
            # execute the SQL query to create a table in the database
            check_table_exist_query = "SHOW TABLES LIKE '" + subject + "_attendance'"
            cursor.execute(check_table_exist_query)
            result = cursor.fetchone()
            if result:
                print("Table exists")
            else:
                create_table_query = "CREATE TABLE if not exists " + subject + "_attendance (ROLLNO varchar(100),Name varchar(100),DATE varchar(50),TIME varchar(50))"
                cursor.execute(create_table_query)
                connection.commit()
            connection.close()

            MESSAGE = tk.Label(MFW, text="Attendance filled Successfully!!!", fg="white", bg="black",
                               width=30, height=2, font=('times', 30, 'italic bold '))
            MESSAGE.place(x=200, y=400)
            enter_data()

    SUB = tk.Label(sb, text="Enter Subject", width=15, height=2, fg="white", bg="black",
                    font=('times', 15))
    SUB.place(x=30, y=100)

    global SUB_ENTRY
    SUB_ENTRY = tk.Entry(sb, width=20, bg="black", fg="white", font=('times', 23))
    SUB_ENTRY.place(x=290, y=105)

    fill_manual_attendance = tk.Button(
        sb, text="Fill Attendance", fg="black", bg="lawn green", width=15, height=2, activebackground="Red", font=('times', 15, ' bold '), command=fill_attendance)
    fill_manual_attendance.place(x=250, y=160)
    sb.mainloop()


def subjectchoose():
    def Fillattendances():
        sub = tx.get()
        now = time.time()  # For calculate seconds of video
        future = now + 20

        if time.time() < future:
            if sub == 'DS':
                DS = "DS Attendance.csv"
                recognizer = cv2.face.LBPHFaceRecognizer_create()
                try:
                    recognizer.read(DS)
                except:
                    e = 'Model not found, please train model'
                    Notifi.configure(text=e)
                harcascadePath = "haarcascade_frontalface_default.xml"
                faceCascade = cv2.CascadeClassifier(harcascadePath)
                df = pd.read_csv(DS)
                cam = cv2.VideoCapture(0)
                font = cv2.FONT_HERSHEY_SIMPLEX
                col_names = ['Enrollment', 'Name']
                attendance = pd.DataFrame(columns=col_names)

                while True:
                    ret, im = cam.read()
                    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                    faces = faceCascade.detectMultiScale(gray, 1.2, 5)

                    for (x, y, w, h) in faces:
                        global Id

                        Id, conf = recognizer.predict(gray[y:y + h, x:x + w])

                        if conf < 73:
                            print(conf)
                            print(id_)
                            global Subject
                            global aa
                            global date
                            global timeStamp
                            global timeStamp
                            Subject = tx.get()
                            ts = time.time()
                            date = datetime.datetime.fromtimestamp(
                                ts).strftime('%Y-%m-%d')
                            timeStamp = datetime.datetime.fromtimestamp(
                                ts).strftime('%H:%M:%S')
                            aa = df.loc[df['Enrollment'] == Id]['Name'].values
                            global tt
                            tt = str(Id) + "-" + aa
                            En = '15624031' + str(Id)
                            attendance.loc[len(attendance)] = [Id, aa]

                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 260, 0), 7)
                            cv2.putText(im, str(tt), (x + h, y), font, 1, (255, 255, 0,), 4)

                        else:
                            Id = 'Unknown'
                            tt = str(Id)
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 7)
                            cv2.putText(im, str(tt), (x + h, y), font, 1, (0, 25, 255), 4)

                    if time.time() > future:
                        break

                    attendance = attendance.drop_duplicates(
                        ['Enrollment'], keep='first')
                    cv2.imshow('Filling attedance..', im)
                    key = cv2.waitKey(30) & 0xff
                    if key == 27:
                        break

                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                Hour, Minute, Second = timeStamp.split(":")
                fileName = "Attendance/" + Subject + "_" + date + "_Time_" + Hour + "-" + Minute + "-" + Second + ".csv"
                attendance = attendance.drop_duplicates(
                    ['Enrollment'], keep='first')
                print(attendance)
                attendance.to_csv(fileName, index=False)

                ##Create table for Attendance
                date_for_DB = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d')
                DB_Table_name = str(Subject + "_" + date_for_DB + "_Time_" + Hour + "_" + Minute + "_" + Second)
                import pymysql.connections

                ###Connect to the database
                try:
                    global cursor
                    connection = pymysql.connect(
                        host='localhost', user='root', password='root', db="Face_reco_fill")
                    cursor = connection.cursor()
                except Exception as e:
                    print(e)

                sql = "CREATE TABLE " + DB_Table_name + """
                                    (ID INT NOT NULL AUTO_INCREMENT,
                                    ENROLLMENT varchar(100) NOT NULL,
                                    NAME VARCHAR(50) NOT NULL,
                                    DATE VARCHAR(20) NOT NULL,
                                    TIME VARCHAR(20) NOT NULL,
                                        PRIMARY KEY (ID)
                                        );
                                    """

                try:
                    cursor.execute(sql)  # for create a table
                except Exception as ex:
                    print(ex)

                # connect to the database
                connect = pymysql.connect(host='localhost', user='root', password='root', database="face_reco_fill")
                # create the object 'cursor' of the class pymysql
                current_cursor = connect.cursor()
                # execute the SQL query to insert the values
                current_cursor.execute("INSERT INTO " + DB_Table_name + " (ID,ENROLLMENT,NAME,DATE,TIME) VALUES (0, %s, %s, %s,%s)", (
                    str(Id), str(aa), str(date), str(timeStamp)))
                # commit the changes
                connect.commit()
                # close the connection
                connect.close()

                import csv
                import tkinter
                root = tkinter.Tk()
                root.title("Attendance of " + Subject)
                root.configure(background='snow')
                cs = 'E:/New folder/Attendance/' + Subject + "_" + date + "_Time_" + Hour + "-" + Minute + "-" + Second + ".csv"
                with open(cs, newline="") as file:
                    reader = csv.reader(file)
                    r = 0
                    for col in reader:
                        c = 0
                        for row in col:
                            # i've added some styling
                            label = tkinter.Label(
                                root, width=8, height=1, fg="black", font=('times', 15, ' bold '), bg="lawn green", text=row, relief=tkinter.RIDGE)
                            label.grid(row=r, column=c)
                            c += 1
                        r += 1
                root.mainloop()
                cam.release()
                cv2.destroyAllWindows()

            elif sub == 'CN':
                CN = "CN Attendance.csv"
                recognizer = cv2.face.LBPHFaceRecognizer_create()
                try:
                    recognizer.read(CN)
                except:
                    e = 'Model not found, please train model'
                    Notifi.configure(text=e)
                harcascadePath = "haarcascade_frontalface_default.xml"
                faceCascade = cv2.CascadeClassifier(harcascadePath)
                df = pd.read_csv(CN)
                cam = cv2.VideoCapture(0)
                font = cv2.FONT_HERSHEY_SIMPLEX
                col_names = ['Enrollment', 'Name']
                attendance = pd.DataFrame(columns=col_names)

                while True:
                    ret, im = cam.read()
                    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                    faces = faceCascade.detectMultiScale(gray, 1.2, 5)

                    for (x, y, w, h) in faces:
                        global Id

                        Id, conf = recognizer.predict(gray[y:y + h, x:x + w])

                        if conf < 73:
                            print(conf)
                            print(id_)
                            global Subject
                            global aa
                            global date
                            global timeStamp
                            global timeStamp
                            Subject = tx.get()
                            ts = time.time()
                            date = datetime.datetime.fromtimestamp(
                                ts).strftime('%Y-%m-%d')
                            timeStamp = datetime.datetime.fromtimestamp(
                                ts).strftime('%H:%M:%S')
                            aa = df.loc[df['Enrollment'] == Id]['Name'].values
                            global tt
                            tt = str(Id) + "-" + aa
                            En = '15624031' + str(Id)
                            attendance.loc[len(attendance)] = [Id, aa]

                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 260, 0), 7)
                            cv2.putText(im, str(tt), (x + h, y), font, 1, (255, 255, 0,), 4)

                        else:
                            Id = 'Unknown'
                            tt = str(Id)
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 7)
                            cv2.putText(im, str(tt), (x + h, y), font, 1, (0, 25, 255), 4)

                    if time.time() > future:
                        break

                    attendance = attendance.drop_duplicates(
                        ['Enrollment'], keep='first')
                    cv2.imshow('Filling attedance..', im)
                    key = cv2.waitKey(30) & 0xff
                    if key == 27:
                        break

                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                Hour, Minute, Second = timeStamp.split(":")
                fileName = "Attendance/" + Subject + "_" + date + "_Time_" + Hour + "-" + Minute + "-" + Second + ".csv"
                attendance = attendance.drop_duplicates(
                    ['Enrollment'], keep='first')
                print(attendance)
                attendance.to_csv(fileName, index=False)

                ##Create table for Attendance
                date_for_DB = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d')
                DB_Table_name = str(Subject + "_" + date_for_DB + "_Time_" + Hour + "_" + Minute + "_" + Second)
                import pymysql.connections

                ###Connect to the database
                try:
                    global cursor
                    connection = pymysql.connect(
                        host='localhost', user='root', password='root', db="Face_reco_fill")
                    cursor = connection.cursor()
                except Exception as e:
                    print(e)

                sql = "CREATE TABLE " + DB_Table_name + """
                                    (ID INT NOT NULL AUTO_INCREMENT,
                                    ENROLLMENT varchar(100) NOT NULL,
                                    NAME VARCHAR(50) NOT NULL,
                                    DATE VARCHAR(20) NOT NULL,
                                    TIME VARCHAR(20) NOT NULL,
                                        PRIMARY KEY (ID)
                                        );
                                    """

                try:
                    cursor.execute(sql)  # for create a table
                except Exception as ex:
                    print(ex)

                # connect to the database
                connect = pymysql.connect(host='localhost', user='root', password='root', database="face_reco_fill")
                # create the object 'cursor' of the class pymysql
                current_cursor = connect.cursor()
                # execute the SQL query to insert the values
                current_cursor.execute("INSERT INTO " + DB_Table_name + " (ID,ENROLLMENT,NAME,DATE,TIME) VALUES (0, %s, %s, %s,%s)", (
                    str(Id), str(aa), str(date), str(timeStamp)))
                # commit the changes
                connect.commit()
                # close the connection
                connect.close()

                import csv
                import tkinter
                root = tkinter.Tk()
                root.title("Attendance of " + Subject)
                root.configure(background='snow')
                cs = 'E:/New folder/Attendance/' + Subject + "_" + date + "_Time_" + Hour + "-" + Minute + "-" + Second + ".csv"
                with open(cs, newline="") as file:
                    reader = csv.reader(file)
                    r = 0
                    for col in reader:
                        c = 0
                        for row in col:
                            # i've added some styling
                            label = tkinter.Label(
                                root, width=8, height=1, fg="black", font=('times', 15, ' bold '), bg="lawn green", text=row, relief=tkinter.RIDGE)
                            label.grid(row=r, column=c)
                            c += 1
                        r += 1
                root.mainloop()
                cam.release()
                cv2.destroyAllWindows()

            elif sub == 'ML':
                ML = "ML Attendance.csv"
                recognizer = cv2.face.LBPHFaceRecognizer_create()
                try:
                    recognizer.read(ML)
                except:
                    e = 'Model not found, please train model'
                    Notifi.configure(text=e)
                harcascadePath = "haarcascade_frontalface_default.xml"
                faceCascade = cv2.CascadeClassifier(harcascadePath)
                df = pd.read_csv(ML)
                cam = cv2.VideoCapture(0)
                font = cv2.FONT_HERSHEY_SIMPLEX
                col_names = ['Enrollment', 'Name']
                attendance = pd.DataFrame(columns=col_names)

                while True:
                    ret, im = cam.read()
                    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                    faces = faceCascade.detectMultiScale(gray, 1.2, 5)

                    for (x, y, w, h) in faces:
                        global Id

                        Id, conf = recognizer.predict(gray[y:y + h, x:x + w])

                        if conf < 73:
                            print(conf)
                            print(id_)
                            global Subject
                            global aa
                            global date
                            global timeStamp
                            global timeStamp
                            Subject = tx.get()
                            ts = time.time()
                            date = datetime.datetime.fromtimestamp(
                                ts).strftime('%Y-%m-%d')
                            timeStamp = datetime.datetime.fromtimestamp(
                                ts).strftime('%H:%M:%S')
                            aa = df.loc[df['Enrollment'] == Id]['Name'].values
                            global tt
                            tt = str(Id) + "-" + aa
                            En = '15624031' + str(Id)
                            attendance.loc[len(attendance)] = [Id, aa]

                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 260, 0), 7)
                            cv2.putText(im, str(tt), (x + h, y), font, 1, (255, 255, 0,), 4)

                        else:
                            Id = 'Unknown'
                            tt = str(Id)
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 7)
                            cv2.putText(im, str(tt), (x + h, y), font, 1, (0, 25, 255), 4)

                    if time.time() > future:
                        break

                    attendance = attendance.drop_duplicates(
                        ['Enrollment'], keep='first')
                    cv2.imshow('Filling attedance..', im)
                    key = cv2.waitKey(30) & 0xff
                    if key == 27:
                        break

                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                Hour, Minute, Second = timeStamp.split(":")
                fileName = "Attendance/" + Subject + "_" + date + "_Time_" + Hour + "-" + Minute + "-" + Second + ".csv"
                attendance = attendance.drop_duplicates(
                    ['Enrollment'], keep='first')
                print(attendance)
                attendance.to_csv(fileName, index=False)

                ##Create table for Attendance
                date_for_DB = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d')
                DB_Table_name = str(Subject + "_" + date_for_DB + "_Time_" + Hour + "_" + Minute + "_" + Second)
                import pymysql.connections

                ###Connect to the database
                try:
                    global cursor
                    connection = pymysql.connect(
                        host='localhost', user='root', password='root', db="Face_reco_fill")
                    cursor = connection.cursor()
                except Exception as e:
                    print(e)

                sql = "CREATE TABLE " + DB_Table_name + """
                                    (ID INT NOT NULL AUTO_INCREMENT,
                                    ENROLLMENT varchar(100) NOT NULL,
                                    NAME VARCHAR(50) NOT NULL,
                                    DATE VARCHAR(20) NOT NULL,
                                    TIME VARCHAR(20) NOT NULL,
                                        PRIMARY KEY (ID)
                                        );
                                    """

                try:
                    cursor.execute(sql)  # for create a table
                except Exception as ex:
                    print(ex)

                # connect to the database
                connect = pymysql.connect(host='localhost', user='root', password='root', database="face_reco_fill")
                # create the object 'cursor' of the class pymysql
                current_cursor = connect.cursor()
                # execute the SQL query to insert the values
                current_cursor.execute("INSERT INTO " + DB_Table_name + " (ID,ENROLLMENT,NAME,DATE,TIME) VALUES (0, %s, %s, %s,%s)", (
                    str(Id), str(aa), str(date), str(timeStamp)))
                # commit the changes
                connect.commit()
                # close the connection
                connect.close()

                import csv
                import tkinter
                root = tkinter.Tk()
                root.title("Attendance of " + Subject)
                root.configure(background='snow')
                cs = 'E:/New folder/Attendance/' + Subject + "_" + date + "_Time_" + Hour + "-" + Minute + "-" + Second + ".csv"
                with open(cs, newline="") as file:
                    reader = csv.reader(file)
                    r = 0
                    for col in reader:
                        c = 0
                        for row in col:
                            # i've added some styling
                            label = tkinter.Label(
                                root, width=8, height=1, fg="black", font=('times', 15, ' bold '), bg="lawn green", text=row, relief=tkinter.RIDGE)
                            label.grid(row=r, column=c)
                            c += 1
                        r += 1
                root.mainloop()
                cam.release()
                cv2.destroyAllWindows()

            elif sub == 'Python':
                Python = "Python Attendance.csv"
                recognizer = cv2.face.LBPHFaceRecognizer_create()
                try:
                    recognizer.read(Python)
                except:
                    e = 'Model not found, please train model'
                    Notifi.configure(text=e)
                harcascadePath = "haarcascade_frontalface_default.xml"
                faceCascade = cv2.CascadeClassifier(harcascadePath)
                df = pd.read_csv(Python)
                cam = cv2.VideoCapture(0)
                font = cv2.FONT_HERSHEY_SIMPLEX
                col_names = ['Enrollment', 'Name']
                attendance = pd.DataFrame(columns=col_names)

                while True:
                    ret, im = cam.read()
                    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                    faces = faceCascade.detectMultiScale(gray, 1.2, 5)

                    for (x, y, w, h) in faces:
                        global Id

                        Id, conf = recognizer.predict(gray[y:y + h, x:x + w])

                        if conf < 73:
                            print(conf)
                            print(id_)
                            global Subject
                            global aa
                            global date
                            global timeStamp
                            global timeStamp
                            Subject = tx.get()
                            ts = time.time()
                            date = datetime.datetime.fromtimestamp(
                                ts).strftime('%Y-%m-%d')
                            timeStamp = datetime.datetime.fromtimestamp(
                                ts).strftime('%H:%M:%S')
                            aa = df.loc[df['Enrollment'] == Id]['Name'].values
                            global tt
                            tt = str(Id) + "-" + aa
                            En = '15624031' + str(Id)
                            attendance.loc[len(attendance)] = [Id, aa]

                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 260, 0), 7)
                            cv2.putText(im, str(tt), (x + h, y), font, 1, (255, 255, 0,), 4)

                        else:
                            Id = 'Unknown'
                            tt = str(Id)
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 7)
                            cv2.putText(im, str(tt), (x + h, y), font, 1, (0, 25, 255), 4)

                    if time.time() > future:
                        break

                    attendance = attendance.drop_duplicates(
                        ['Enrollment'], keep='first')
                    cv2.imshow('Filling attedance..', im)
                    key = cv2.waitKey(30) & 0xff
                    if key == 27:
                        break

                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                Hour, Minute, Second = timeStamp.split(":")
                fileName = "Attendance/" + Subject + "_" + date + "_Time_" + Hour + "-" + Minute + "-" + Second + ".csv"
                attendance = attendance.drop_duplicates(
                    ['Enrollment'], keep='first')
                print(attendance)
                attendance.to_csv(fileName, index=False)

                ##Create table for Attendance
                date_for_DB = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d')
                DB_Table_name = str(Subject + "_" + date_for_DB + "_Time_" + Hour + "_" + Minute + "_" + Second)
                import pymysql.connections

                ###Connect to the database
                try:
                    global cursor
                    connection = pymysql.connect(
                        host='localhost', user='root', password='root', db="Face_reco_fill")
                    cursor = connection.cursor()
                except Exception as e:
                    print(e)

                sql = "CREATE TABLE " + DB_Table_name + """
                                    (ID INT NOT NULL AUTO_INCREMENT,
                                    ENROLLMENT varchar(100) NOT NULL,
                                    NAME VARCHAR(50) NOT NULL,
                                    DATE VARCHAR(20) NOT NULL,
                                    TIME VARCHAR(20) NOT NULL,
                                        PRIMARY KEY (ID)
                                        );
                                    """

                try:
                    cursor.execute(sql)  # for create a table
                except Exception as ex:
                    print(ex)

                # connect to the database
                connect = pymysql.connect(host='localhost', user='root', password='root', database="face_reco_fill")
                # create the object 'cursor' of the class pymysql
                current_cursor = connect.cursor()
                # execute the SQL query to insert the values
                current_cursor.execute("INSERT INTO " + DB_Table_name + " (ID,ENROLLMENT,NAME,DATE,TIME) VALUES (0, %s, %s, %s,%s)", (
                    str(Id), str(aa), str(date), str(timeStamp)))
                # commit the changes
                connect.commit()
                # close the connection
                connect.close()

                import csv
                import tkinter
                root = tkinter.Tk()
                root.title("Attendance of " + Subject)
                root.configure(background='snow')
                cs = 'E:/New folder/Attendance/' + Subject + "_" + date + "_Time_" + Hour + "-" + Minute + "-" + Second + ".csv"
                with open(cs, newline="") as file:
                    reader = csv.reader(file)
                    r = 0
                    for col in reader:
                        c = 0
                        for row in col:
                            # i've added some styling
                            label = tkinter.Label(
                                root, width=8, height=1, fg="black", font=('times', 15, ' bold '), bg="lawn green", text=row, relief=tkinter.RIDGE)
                            label.grid(row=r, column=c)
                            c += 1
                        r += 1
                root.mainloop()
                cam.release()
                cv2.destroyAllWindows()

            elif sub == 'Java':
                Java = "Java Attendance.csv"
                recognizer = cv2.face.LBPHFaceRecognizer_create()
                try:
                    recognizer.read(Java)
                except:
                    e = 'Model not found, please train model'
                    Notifi.configure(text=e)
                harcascadePath = "haarcascade_frontalface_default.xml"
                faceCascade = cv2.CascadeClassifier(harcascadePath)
                df = pd.read_csv(Java)
                cam = cv2.VideoCapture(0)
                font = cv2.FONT_HERSHEY_SIMPLEX
                col_names = ['Enrollment', 'Name']
                attendance = pd.DataFrame(columns=col_names)

                while True:
                    ret, im = cam.read()
                    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                    faces = faceCascade.detectMultiScale(gray, 1.2, 5)

                    for (x, y, w, h) in faces:
                        global Id

                        Id, conf = recognizer.predict(gray[y:y + h, x:x + w])

                        if conf < 73:
                            print(conf)
                            print(id_)
                            global Subject
                            global aa
                            global date
                            global timeStamp
                            global timeStamp
                            Subject = tx.get()
                            ts = time.time()
                            date = datetime.datetime.fromtimestamp(
                                ts).strftime('%Y-%m-%d')
                            timeStamp = datetime.datetime.fromtimestamp(
                                ts).strftime('%H:%M:%S')
                            aa = df.loc[df['Enrollment'] == Id]['Name'].values
                            global tt
                            tt = str(Id) + "-" + aa
                            En = '15624031' + str(Id)
                            attendance.loc[len(attendance)] = [Id, aa]

                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 260, 0), 7)
                            cv2.putText(im, str(tt), (x + h, y), font, 1, (255, 255, 0,), 4)

                        else:
                            Id = 'Unknown'
                            tt = str(Id)
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 7)
                            cv2.putText(im, str(tt), (x + h, y), font, 1, (0, 25, 255), 4)

                    if time.time() > future:
                        break

                    attendance = attendance.drop_duplicates(
                        ['Enrollment'], keep='first')
                    cv2.imshow('Filling attedance..', im)
                    key = cv2.waitKey(30) & 0xff
                    if key == 27:
                        break

                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                Hour, Minute, Second = timeStamp.split(":")
                fileName = "Attendance/" + Subject + "_" + date + "_Time_" + Hour + "-" + Minute + "-" + Second + ".csv"
                attendance = attendance.drop_duplicates(
                    ['Enrollment'], keep='first')
                print(attendance)
                attendance.to_csv(fileName, index=False)

                ##Create table for Attendance
                date_for_DB = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d')
                DB_Table_name = str(Subject + "_" + date_for_DB + "_Time_" + Hour + "_" + Minute + "_" + Second)
                import pymysql.connections

                ###Connect to the database
                try:
                    global cursor
                    connection = pymysql.connect(
                        host='localhost', user='root', password='root', db="Face_reco_fill")
                    cursor = connection.cursor()
                except Exception as e:
                    print(e)

                sql = "CREATE TABLE " + DB_Table_name + """
                                    (ID INT NOT NULL AUTO_INCREMENT,
                                    ENROLLMENT varchar(100) NOT NULL,
                                    NAME VARCHAR(50) NOT NULL,
                                    DATE VARCHAR(20) NOT NULL,
                                    TIME VARCHAR(20) NOT NULL,
                                        PRIMARY KEY (ID)
                                        );
                                    """

                try:
                    cursor.execute(sql)  # for create a table
                except Exception as ex:
                    print(ex)

                # connect to the database
                connect = pymysql.connect(host='localhost', user='root', password='root', database="face_reco_fill")
                # create the object 'cursor' of the class pymysql
                current_cursor = connect.cursor()
                # execute the SQL query to insert the values
                current_cursor.execute("INSERT INTO " + DB_Table_name + " (ID,ENROLLMENT,NAME,DATE,TIME) VALUES (0, %s, %s, %s,%s)", (
                    str(Id), str(aa), str(date), str(timeStamp)))
                # commit the changes
                connect.commit()
                # close the connection
                connect.close()

                import csv
                import tkinter
                root = tkinter.Tk()
                root.title("Attendance of " + Subject)
                root.configure(background='snow')
                cs = 'E:/New folder/Attendance/' + Subject + "_" + date + "_Time_" + Hour + "-" + Minute + "-" + Second + ".csv"
                with open(cs, newline="") as file:
                    reader = csv.reader(file)
                    r = 0
                    for col in reader:
                        c = 0
                        for row in col:
                            # i've added some styling
                            label = tkinter.Label(
                                root, width=8, height=1, fg="black", font=('times', 15, ' bold '), bg="lawn green", text=row, relief=tkinter.RIDGE)
                            label.grid(row=r, column=c)
                            c += 1
                        r += 1
                root.mainloop()
                cam.release()
                cv2.destroyAllWindows()

            else:
                Notifica.configure(text="Please enter valid subject name", bg="SpringGreen3",
                                   fg="black", width=33, font=('times', 19, 'bold'))
                Notifica.place(x=170, y=380)

    sb = tk.Tk()
    sb.geometry('580x320')
    sb.title('Enter subject name...')

    sb.configure(background='snow')

    Notifica = tk.Label(sb, text="Attendance filled Successfully", bg="Green", fg="white", width=33,
                        height=2, font=('times', 19, 'bold'))

    def Attf():
        import subprocess
        subprocess.Popen(
            r'explorer /select,"E:/New folder/Attendace files/----Check atttendance-------"')

    attf = tk.Button(sb, text="Check Sheets", command=Attf, fg="black", bg="lawn green", width=15,
                     height=1, activebackground="Red", font=('times', 14, ' bold '))
    attf.place(x=425, y=255)

    quitWindow = tk.Button(sb, text="Quit", command=sb.destroy, fg="black", bg="red", width=10,
                           height=1, activebackground="Red", font=('times', 14, ' bold '))
    quitWindow.place(x=485, y=25)

    tx = tk.StringVar()
    tx.set("Enter here")
    SUB = tk.Label(sb, text="Enter Subject", width=15, height=2, fg="white", bg="black",
                   font=('times', 15))
    SUB.place(x=30, y=50)

    sb = tk.Entry(sb, textvar=tx, width=20, bg="black", fg="white", font=('times', 23))
    sb.place(x=290, y=55)

    fill_manual_attendance = tk.Button(
        sb, text="Fill Attendance", fg="black", bg="lawn green", width=15, height=2, activebackground="Red", font=('times', 15, ' bold '), command=Fillattendances)
    fill_manual_attendance.place(x=250, y=155)

    sb.mainloop()


def admin_panel():
    window_admin = tk.Tk()
    window_admin.iconbitmap('AMS.ico')
    window_admin.title("Admin Login")
    window_admin.geometry('580x320')
    window_admin.configure(background='snow')

    def log_in():
        username = un_entr.get()
        password = pw_entr.get()

        if username == 'tanishq' :
            if password == 'tanishq':
                window_admin.destroy()
                import csv
                import tkinter
                root = tkinter.Tk()
                root.title("Student Details")
                root.configure(background='snow')

                cs = 'E:/New folder/StudentDetails/StudentDetails.csv'
                with open(cs, newline="") as file:
                    reader = csv.reader(file)
                    r = 0
                    for col in reader:
                        c = 0
                        for row in col:
                            # i've added some styling
                            label = tkinter.Label(
                                root, width=8, height=1, fg="black", font=('times', 15, ' bold '), bg="lawn green", text=row, relief=tkinter.RIDGE)
                            label.grid(row=r, column=c)
                            c += 1
                        r += 1
                root.mainloop()
            else:
                valid = 'Incorrect ID or Password'
                Nt.configure(text=valid, bg="red", fg="black", width=30, font=('times', 19, 'bold'))
                Nt.place(x=90, y=290)
        else:
            valid = 'Incorrect ID or Password'
            Nt.configure(text=valid, bg="red", fg="black", width=30, font=('times', 19, 'bold'))
            Nt.place(x=90, y=290)

    Nt = tk.Label(window_admin, text="Attendance filled Successfully", bg="Green", fg="white", width=33,
                  height=2, font=('times', 19, 'bold'))

    un = tk.Label(window_admin, text="Enter Username", width=15, height=2, fg="white", bg="black",
                  font=('times', 15))
    un.place(x=30, y=50)

    pw = tk.Label(window_admin, text="Enter Password", width=15, height=2, fg="white", bg="black",
                  font=('times', 15))
    pw.place(x=30, y=150)

    def c00():
        un_entr.delete(first=0, last=22)

    un_entr = tk.Entry(window_admin, width=20, bg="black", fg="white", font=('times', 23))
    un_entr.place(x=290, y=55)

    def c11():
        pw_entr.delete(first=0, last=22)

    pw_entr = tk.Entry(window_admin, width=20, bg="black", fg="white", font=('times', 23))
    pw_entr.place(x=290, y=155)

    c0 = tk.Button(window_admin, text="Clear", command=c00, fg="black", bg="deep pink", width=10, height=1,
                   activebackground="Red", font=('times', 15, ' bold '))
    c0.place(x=490, y=55)

    c1 = tk.Button(window_admin, text="Clear", command=c11, fg="black", bg="deep pink", width=10, height=1,
                   activebackground="Red", font=('times', 15, ' bold '))
    c1.place(x=490, y=155)

    Login = tk.Button(window_admin, text="LogIn", fg="black", bg="lawn green", width=20,
                      height=2, activebackground="Red", font=('times', 15, ' bold '), command=log_in)
    Login.place(x=290, y=230)
    window_admin.mainloop()

def contact_us():
    import webbrowser
    webbrowser.open('https://www.google.com')


def developer():
    import tkinter.messagebox
    tkinter.messagebox.showinfo('Developer', 'This software was made by Tanishq Chamoli.')


def visit_website():
    import webbrowser
    webbrowser.open('https://www.google.com')


def exitt():
    MsgBox = tk.messagebox.askquestion(
        'Exit Application', 'Are you sure you want to exit the application', icon='warning')
    if MsgBox == 'yes':
        tk.messagebox.showinfo(
            "Greetings", "Thank You very much for using our software. Have a good day ahead!!")
        root.destroy()
    else:
        tk.messagebox.showinfo('Return', 'You will now return to the application screen')


root = tk.Tk()
root.title('Face Recogniser')

root.configure(background='snow')

root.geometry('1280x720')

root.iconbitmap('AMS.ico')

root.resizable(False, False)

TakeImg = tk.Button(root, text="Check Sheets", command=admin_panel, fg="white", bg="blue2", width=20, height=3,
                    activebackground="Red", font=('times', 15, ' bold '))
TakeImg.place(x=200, y=200)

Start = tk.Button(root, text="Take Attendance", command=Fillattendances, fg="white", bg="blue2", width=20, height=3,
                   activebackground="Red", font=('times', 15, ' bold '))
Start.place(x=500, y=200)

Q = tk.Button(root, text="Quit", command=exitt, fg="white", bg="blue2", width=20, height=3,
              activebackground="Red", font=('times', 15, ' bold '))
Q.place(x=800, y=200)

root.mainloop()
