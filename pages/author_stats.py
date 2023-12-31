import streamlit as st
import backend
import altair as alt
import pandas as pd

st.title('Author Stats')


def author_chart(data):
    chart = alt.Chart(data, title='Books by Author').mark_bar().encode(
        x=alt.X('Author', sort='-y'),
        y=alt.Y('Book Title', title=None)
    )

    return chart


data = backend.books
books_read = data[data['Status'] == 'Read']
author_list = books_read.groupby('Author')['Book Title'].count().sort_values(ascending=False).to_frame().reset_index()

st.altair_chart(author_chart(author_list))
