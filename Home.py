import streamlit as st
import backend

st.set_page_config(page_title='Reading Tracker- Home')
st.title('Reading Tracker')

st.text("Welcome to Alan's Reading Tracking App!")
st.text('Use the menu to the left to navigate through the app')

users = ['Alan', 'Michaels', 'Jeff']
selected_user = st.selectbox('View stats for:', users)


if "book_data" not in st.session_state or st.button('Confirm User'):
    status = st.text('Loading Data')
    st.session_state.book_data, st.session_state.log_data = backend.load_data(selected_user)  # 👈 Download the data
    status.text('Data loaded')

with st.expander('Click here to view the raw data'):
    st.header('Book Data')
    st.write(st.session_state.book_data)

    st.header('Log Data')
    st.write(st.session_state.log_data)

book_formats = ['Book', 'eBook', 'Audiobook']
current_books = st.session_state.book_data[st.session_state.book_data['status'] == 'Currently Reading']['book_title'].to_list()

with st.expander('Add New Book Entry'):
    with st.form('New Book'):
        book_col_left, book_col_mid, book_col_right = st.columns(3)
        status_col_left, status_col_right = st.columns([2,1])
        with book_col_left:
            book_title = st.text_input('Book Title*')
            series = st.text_input('Series')
            start_date = st.date_input('Start Date')
        with book_col_mid:
            author = st.text_input('Author*')
            series_ranking = st.number_input('Series Ranking', min_value=1, step=1, format='%i')
            # st.text('')
            finish_date = st.date_input('Finish Date')
        with book_col_right:
            pages = st.number_input('Pages*', min_value=1, step=1, format='%i')
            genre = st.selectbox('Genre', options=['Fantasy', 'Crime'])
            # st.markdown('#')
            st.text_input('Reading Pace', placeholder='50 pages/day', disabled=True)
        with status_col_left:
            status = st.selectbox('Status*', ['Read', 'Currently Reading', 'DNF', 'To Read'])
        with status_col_right:
            format = st.selectbox('Format*', book_formats)
        book_submitted = st.form_submit_button("Submit")

with st.expander('Add New Log Entry'):
    with st.form('New Log Entry'):
        date = st.date_input('Date*', value='today')
        log_col_left, log_col_right = st.columns(2)
        with log_col_left:
            log_book = st.selectbox('Book Title*', current_books)
            start_page = st.number_input('Start Page*', min_value=1, step=1, format='%i')
        with log_col_right:
            log_format = st.selectbox('Format*', book_formats)
            end_page = st.number_input('End Page', value=None, min_value=start_page+1, step=1, format='%i')
        log_submitted = st.form_submit_button("Submit")

