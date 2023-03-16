import streamlit as st
import pandas as pd
import numpy as np
import regestration, attendence, details
#  ----------------  main.py ---------------

st.set_page_config(page_title="attendace system", layout="wide")

# -- creating the main page

dict_1 = {"Student Regestration": regestration,"Attendance": attendence,"details": details}

# making a sidebar and displaying the apps

with st.sidebar:
    radio = st.radio(label="change the app here", options= list(dict_1.keys()))

dict_1[radio].app()  # calling differnt pages
