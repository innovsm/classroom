import streamlit as st
import cv2
import numpy as np
import mysql.connector
import face_recognition

def insert_student_info(name, roll_number, unique_id):
    try:
        my_db_2 = mysql.connector.connect(
            host="sql.freedb.tech",
            user="freedb_alfa_adv",
            password="eaV%K&6V$FDj2rt",
            database="freedb_attendence"
        )
        my_cursor = my_db_2.cursor()

        sql = "INSERT INTO student_info (name, roll_number, unique_id) VALUES (%s, %s, %s)"
        val = (name, roll_number, unique_id)

        my_cursor.execute(sql, val)
        my_db_2.commit()

        #print(my_cursor.rowcount, "record inserted.")

    except mysql.connector.Error as error:
        print("Failed to insert record into student_info table: {}".format(error))

    finally:
        if (my_db_2.is_connected()):
            my_cursor.close()
            my_db_2.close()
            print("MySQL connection is closed.")


def upload_data(name,roll_number,image,model_face):
    # getting face - encoding s

    frame_gray  = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    faces =  model_face.detectMultiScale(frame_gray)
    #print(len(faces))
    x, y, w, h = faces[0]  # this is for single person regestration
    
    face_encoding = face_recognition.face_encodings(image[y:y+h,x:x+w][:,:,::-1])
    #print(face_encoding[0].shape)

    insert_student_info(name, roll_number, str(face_encoding[0]))
    st.write("successfuly registered")

    


#----- 
def app():
    model_face = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml") # model declaration 


    st.title("Attendence")
    st.header("Enter the details below")
    
    with st.form(key = "student_data"):
        name = st.text_input("Enter you name",max_chars=70)
        roll_number = st.text_input("Enter your roll number",max_chars=30)
        image = st.camera_input("provide your image")
        submit_button = st.form_submit_button(label="submit")

 
        if submit_button:
             if image is not None:
                 bytes_data = image.getvalue()
                 
                 cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
            
                 upload_data(name,roll_number,cv2_img,model_face)
                 # processing will begin here 
                 st.write(name,roll_number)

    
        

                


