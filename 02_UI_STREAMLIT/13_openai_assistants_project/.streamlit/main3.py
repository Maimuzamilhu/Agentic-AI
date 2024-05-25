import streamlit as st
import plotly.graph_objects as go

st.title("Map Gpt")

left_col , right_col = st.columns(2)

with left_col:
    st.subheader("Conversations")
