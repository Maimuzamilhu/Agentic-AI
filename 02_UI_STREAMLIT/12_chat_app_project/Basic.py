import streamlit as st
import numpy as np


"""with st.chat_message("User"):
    st.write("Hello Muzzamil 👋")

with st.chat_message("assistant"):
    st.write("Hello Human")
    st.bar_chart(np.random.randn(30, 3))


prompt = st.chat_input("Say Something")
if prompt:
    st.write(f"User has send the following : {prompt}")



st.title("Muzzamil Bot")

if "message" not in st.session_state: #Agr phly us dic mai nhi hai tbhi add krna hai new value ko
    st.session_state.message = []

for message in st.session_state.message:
    with st.chat_message(message["Hello"]):
        st.markdown(message["Content"])
#Another Example
if 'counter' not in st.session_state:
    st.session_state['counter'] = 0

# Increment the counter when the button is pressed
if st.button('Click me!'):
    st.session_state['counter'] += 1

st.write('Button has been clicked', st.session_state['counter'], 'times')
"""

"""Prompt user"""
if prompt := st.chat_input("What is up?"):
    #Display user msg
    with st.chat_message("user"):
        st.markdown(prompt)

st.session_state.message.append({"role":"user", "content" : prompt})