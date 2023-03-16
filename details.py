import pandas as pd
import numpy as np
import mysql.connector
from datetime import datetime
import streamlit as st

def app():
    st.title("overall attendance")
    my_db_2 = mysql.connector.connect(
        host="sql.freedb.tech",
        user="freedb_alfa_adv",
        password="eaV%K&6V$FDj2rt",
        database="freedb_attendence"
        )
   
    cursor = my_db_2.cursor()
    cursor.execute("SELECT * FROM  attendance")
    result = cursor.fetchall()
    data = pd.DataFrame(result,columns=['date', 'roll_number', 'attendence'])
    data.drop_duplicates(inplace=True)
    st.write(data)