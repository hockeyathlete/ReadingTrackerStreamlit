import streamlit as st
import backend

st.set_page_config(page_title='Reading Tracker- Home')
st.title('Reading Tracker')

st.text("Welcome to Alan's Reading Tracking App!")
st.text('Use the menu to the left to navigate through the app')


if "book_data" not in st.session_state:
    status = st.text('Loading Data')
    st.session_state.book_data, st.session_state.log_data = backend.load_data()  # 👈 Download the data

with st.expander('Click here to view the raw data'):
    st.header('Book Data')
    st.write(st.session_state.book_data)

    st.header('Log Data')
    st.write(st.session_state.log_data)
