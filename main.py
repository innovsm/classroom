import streamlit as st
from deepface import DeepFace

st.write(DeepFace.verify("test.jpg", "gama.jpg"))
