import streamlit as st
import altair as alt

def author_chart(author_data):
    chart = alt.Chart(author_data, title='Books by Author').mark_bar().encode(
        x=alt.X('author', sort='-y'),
        y=alt.Y('book_title', title=None)
    )

    return chart

st.set_page_config(page_title='Reading Tracker- Author Stats')
st.title('Author Stats')


data = st.session_state.book_data
books_read = data[data['status'] == 'Read']
author_list = books_read.groupby('author')['book_title'].count().sort_values(ascending=False).to_frame().reset_index()

st.altair_chart(author_chart(author_list))
