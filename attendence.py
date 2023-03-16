import streamlit as st 
import pandas as pd
import numpy as np
import mysql.connector
from datetime import datetime
import pytz
import ast
import face_recognition
import cv2
model_face = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")

# ---------- all functions -------------
def clear_image_table():
    my_db_2 = mysql.connector.connect(
        host="sql.freedb.tech",
        user="freedb_alfa_adv",
        password="eaV%K&6V$FDj2rt",
        database="freedb_attendence"
        )
    mycursor = my_db_2.cursor()
    sql = "TRUNCATE TABLE images"
    my_db_2.commit()
    mycursor.execute(sql)

def clear_student_table():
    my_db_2 = mysql.connector.connect(
        host="sql.freedb.tech",
        user="freedb_alfa_adv",
        password="eaV%K&6V$FDj2rt",
        database="freedb_attendence"
        )
    mycursor = my_db_2.cursor()
    sql = "TRUNCATE TABLE student_info"
    my_db_2.commit()
    mycursor.execute(sql)

def image_encoding(frame,model_face):
    frame_gray  = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces =  model_face.detectMultiScale(frame_gray)
    final_array  = []
    for face in faces:
        x,y,w,h = face
        detected_face = face_recognition.face_encodings(frame[y:y+h,x:x+w][:,:,::-1])
        final_array.append(detected_face)
    return final_array
def get_final_encoding():
    my_db_2 = mysql.connector.connect(
        host="sql.freedb.tech",
        user="freedb_alfa_adv",
        password="eaV%K&6V$FDj2rt",
        database="freedb_attendence"
    )
    my_cursor = my_db_2.cursor()
    sql = "SELECT * FROM images"
    my_cursor.execute(sql)
    myresult = my_cursor.fetchall()
    final_list = []
    for x in myresult:
        final_list.append(x)
    print(len(final_list))
    final_dataset = []
    for i in range(len(final_list)):
        image_data = final_list[i][2]
        nparr = np.frombuffer(image_data, np.uint8)
        print(nparr)
        try:
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)   # getting the gray-scale image
            print(img.shape)

            #cv2.imwrite("alfa.jpg", img)
            #print(img.shape)
            #print("1")
            final_dataset.append(image_encoding(img, model_face))
            #print("2")
        except:
            #print("EOFError")
            continue
    return final_dataset

def get_student_details():
   my_db_2 = mysql.connector.connect(
      host="sql.freedb.tech",
      user="freedb_alfa_adv",
      password="eaV%K&6V$FDj2rt",
      database="freedb_attendence"
      )
   my_cursor = my_db_2.cursor()
   sql = "SELECT * FROM student_info"
   my_cursor.execute(sql)
   result = my_cursor.fetchall()
   data = pd.DataFrame(result,columns=['student_name', 'roll_number', 'unique_id'])
   return data

def refined_dataset(string_arr):
    data_1 = string_arr.split(" ")
    final_array = []
    for i in data_1:
        if(i != ""):
            if("[" in i):
                data = i.replace('[', "")
                final_array.append(ast.literal_eval(data))
            elif(']' in i):
                data = i.replace("]", "")
                final_array.append(ast.literal_eval(data))
            else:
                final_array.append(ast.literal_eval(i))
    return np.array(final_array)

def apply_1(i,list_1):
    if(i in list_1):
        return 1
    else:
        return 0

def save_dataframe(list_1):

    my_db_2 = mysql.connector.connect(
        host="sql.freedb.tech",
        user="freedb_alfa_adv",
        password="eaV%K&6V$FDj2rt",
        database="freedb_attendence"
        )
    sql = "INSERT INTO attendance (date ,roll_number ,attendance) VALUES (%s, %s, %s)"
    cursor = my_db_2.cursor()
    val = (list_1[0], list_1[1],str(list_1[2]))
    cursor.execute(sql,val)
    my_db_2.commit()


def get_attendence():
    data_image_captured = get_final_encoding()
    data_student = get_student_details()
    data = list(data_student['unique_id'])
    student_refined = []
    for i in data:
        student_refined.append(refined_dataset(i))
    data_student['facial_id'] = student_refined
    student_list = list(data_student['facial_id'])  # got index of student
    total_student = len(student_list)
    student_present = []
    for i in data_image_captured:
        if(len(i) == 0):
            continue
        else:
            for j in range(len(student_list)):
                if(total_student == 0):   # codition breaker
                    break
                if(True in face_recognition.compare_faces(i[0], student_list[j])):
                    total_student = total_student -1
                    student_present.append(j)
                    print(data_student.iloc[j]['student_name'])
    data_student['PRIMARY_KEY'] = data_student.index
    data_student['attendence'] = data_student['PRIMARY_KEY'].apply(apply_1,args = (student_present,))
    timezone = pytz.timezone("Asia/Kolkata")
    date_now = datetime.now(timezone)
    now = date_now.strftime('%Y-%m-%d')
    data_student['date'] = [str(now)]*len(data_student)
    clear_image_table()  # clear images table
    alfa =  data_student[['date','student_name', 'roll_number', 'attendence']]
    data_date = list(alfa['date'])
    data_roll = list(alfa['roll_number'])
    data_attendence = list(alfa['attendence'])
    for i in list(zip(data_date,data_roll, data_attendence)):
        save_dataframe(i)
    print("data saved")
    
    return alfa


def app():
    st.title("Attendence System")
    st.header("Below is the link to access the camera")
    st.markdown("camera-link(https://alternative2.onrender.com)")

    checkbox = st.checkbox("get attendence")
    if(checkbox):
        st.write(get_attendence())
        

