import streamlit as st
import backend


st.title('Book Tracker')

if "book_data" not in st.session_state:
    status = st.text('Loading Data')
    st.session_state.book_data, st.session_state.log_data = backend.load_data()  # 👈 Download the data

st.header('Book Data')
st.write(st.session_state.book_data)

st.header('Log Data')
st.write(st.session_state.log_data)
