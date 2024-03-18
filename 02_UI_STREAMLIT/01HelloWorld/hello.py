import streamlit as st

# Check all the commands from cheatsheat streamlit

st.text("Hello , world")
st.write("Write text demo")
st.title("The Muzzamil Khalid ChatBot")

st.markdown("# Markdown Heading")

st.latex(r""" e^{i\pi} + 1 = 0 """) #WE USE THIS FOR RESEACH PAPERS

st.header("My header")
st.subheader("My sub")
st.code("for i in range(8): foo()")

#for add video via link

st.video("https://www.youtube.com/watch?v=olbRZroz824")
st.image("https://img2.thejournal.ie/inline/5862189/original/?width=630&version=5862189")