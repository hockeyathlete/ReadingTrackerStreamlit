import streamlit as st
import backend
import pandas as pd


def book_form(key, book_data=None):
    if not book_data:
        book_data = {'book_title': None, 'author': None, 'start_date': 'today', 'finish_date': None,
                     'status': 'Currently Reading', 'pages': 1, 'series': None, 'series_ranking': None,
                     'genre': 'Fantasy', 'format': 'Book'}

    form = st.form(key)

    # Pandas doesn't use mixed int and NaN type columns, so have to convert the series ranking to int if it's NaN
    try:
        book_data['series_ranking'] = int(book_data['series_ranking'])
    except (TypeError, ValueError):
        book_data['series_ranking'] = None

    if str(book_data['finish_date']) == 'NaT':
        book_data['finish_date'] = None

    book_col_left, book_col_mid, book_col_right = form.columns(3)
    status_col_left, status_col_right = form.columns([2, 1])

    book_title = book_col_left.text_input('Book Title*', value=book_data['book_title'])
    author = book_col_mid.text_input('Author*', value=book_data['author'])
    pages = book_col_right.number_input('Pages*', min_value=1, value=book_data['pages'], step=1, format='%i')

    series = book_col_left.text_input('Series', value=book_data['series'])
    series_ranking = book_col_mid.number_input('Series Ranking', min_value=1, value=book_data['series_ranking'], step=1, format='%i')
    genre_index = genres.index(book_data['genre'])
    genre = book_col_right.selectbox('Genre', options=genres, index=genre_index)

    start_date = book_col_left.date_input('Start Date', value=book_data['start_date'])
    finish_date = book_col_mid.date_input('Finish Date', value=book_data['finish_date'])
    book_col_right.text_input('Reading Pace', placeholder='50 pages/day', disabled=True)

    status = status_col_left.selectbox('Status*', ['Read', 'Currently Reading', 'DNF', 'To Read'])
    format = status_col_right.selectbox('Format*', book_formats)

    book_submitted = form.form_submit_button(key)
    return form


def log_form(key, log_data=None, index=0):
    if not log_data:
        log_data = {'date': 'today', 'book_title': None, 'start_page': 1, 'end_page': None}

    form = st.form(key)
    date = form.date_input('Date*', value=log_data['date'])
    log_col_left, log_col_right = form.columns(2)
    log_book = log_col_left.selectbox('Book Title*', full_book_list_reversed, index=index)
    start_page = log_col_left.number_input('Start Page*', value=log_data['start_page'], min_value=1, step=1,
                                           format='%i')
    log_format = log_col_right.selectbox('Format*', book_formats)
    end_page = log_col_right.number_input('End Page', value=log_data['end_page'], min_value=start_page + 1, step=1,
                                          format='%i')
    log_submitted = form.form_submit_button(key)
    return form


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
### UPDATE FROM READ TO CURRENTLY READING ###
current_books = st.session_state.book_data[st.session_state.book_data['status'] == 'Read'][
    'book_title'].to_list()
full_book_list_reversed = st.session_state.book_data['book_title'].iloc[::-1].to_list()
### NEED TO ADD MORE GENRES ###
genres = ['Fantasy', 'Sci-fi', 'Crime']

with st.expander('Add New Book Entry'):
    book_form('Add Book')

with st.expander('Add New Log Entry'):
    log_form('Add Log Entry')

with st.expander('Edit Book'):
    book_selected = st.selectbox('Select a book', full_book_list_reversed, key='book_edit_selectbox')
    book_info = st.session_state.book_data[st.session_state.book_data['book_title'] == book_selected]
    book_form('Edit Book', book_data=book_info.squeeze().to_dict())

with st.expander('Edit Log'):
    book_selected = st.selectbox('Select a book', full_book_list_reversed, key='log_edit_selectbox')
    book_selected_index = full_book_list_reversed.index(book_selected)
    selected_logs = st.session_state.log_data[st.session_state.log_data['book_title'] == book_selected]
    selected_log = st.radio('Log', selected_logs['date'].dt.strftime('%m/%d/%Y'),
                            captions=selected_logs['format'] + ': Page ' + selected_logs['start_page'].astype(str) + ' to ' +
                                     selected_logs['end_page'].astype(str))
    log_form('Edit Log Entry', selected_logs[(selected_logs['date'] == selected_log)].squeeze().to_dict(),
             index=book_selected_index)
