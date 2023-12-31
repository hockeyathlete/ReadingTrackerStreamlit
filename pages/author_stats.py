import streamlit as st
import altair as alt

st.title('Author Stats')


def author_chart(author_data):
    chart = alt.Chart(author_data, title='Books by Author').mark_bar().encode(
        x=alt.X('Author', sort='-y'),
        y=alt.Y('Book Title', title=None)
    )

    return chart


data = st.session_state.book_data
books_read = data[data['Status'] == 'Read']
author_list = books_read.groupby('Author')['Book Title'].count().sort_values(ascending=False).to_frame().reset_index()

st.altair_chart(author_chart(author_list))
