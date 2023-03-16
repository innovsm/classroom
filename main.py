import streamlit as st
from deepface import DeepFace


from deepface import DeepFace

# Load the VGG-Face model weights
model = DeepFace.build_model('VGG-Face')

# Verify two faces using the VGG-Face model
result = DeepFace.verify("test.jpg", "gama.jpg", model=model)

# Print the verification result
st.write(result)
