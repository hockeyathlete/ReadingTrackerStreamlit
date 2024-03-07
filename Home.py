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
current_books = st.session_state.book_data[st.session_state.book_data['status'] == 'Read'][
    'book_title'].to_list()
full_book_list_reversed = st.session_state.book_data['book_title'].iloc[::-1].to_list()

with st.expander('Add New Book Entry'):
    with st.form('New Book'):
        book_col_left, book_col_mid, book_col_right = st.columns(3)
        status_col_left, status_col_right = st.columns([2, 1])
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


def log_form(key, default_data=None, index=0):
    if not default_data:
        default_data = {'date': 'today', 'book_title': None, 'start_page': 1, 'end_page': None}

    form = st.form(key)
    date = form.date_input('Date*', value=default_data['date'])
    log_col_left, log_col_right = form.columns(2)
    log_book = log_col_left.selectbox('Book Title*', full_book_list_reversed, index=index)
    start_page = log_col_left.number_input('Start Page*', value=default_data['start_page'], min_value=1, step=1,
                                           format='%i')
    log_format = log_col_right.selectbox('Format*', book_formats)
    end_page = log_col_right.number_input('End Page', value=default_data['end_page'], min_value=start_page + 1, step=1,
                                          format='%i')
    log_submitted = form.form_submit_button(key)
    return form


with st.expander('Add New Log Entry'):
    log_form('Add Log Entry')

with st.expander('Edit Log'):
    book_selected = st.selectbox('Select a book', full_book_list_reversed)
    book_logs = st.session_state.log_data[st.session_state.log_data['book_title'] == book_selected]
    selected_log = st.radio('Log', book_logs['date'].dt.strftime('%m/%d/%Y'),
                            captions=book_logs['format'] + ': Page ' + book_logs['start_page'].astype(str) + ' to ' +
                                     book_logs['end_page'].astype(str))
    log_form('Edit Log Entry', book_logs[(book_logs['date'] == selected_log)].squeeze().to_dict(),
             index=full_book_list_reversed.index(book_selected))
