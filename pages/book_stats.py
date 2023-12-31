import pandas as pd
import altair as alt
import streamlit as st

def books_by_year_chart(books_by_year_data):
    chart = alt.Chart(books_by_year, title='Books by Year').mark_bar().encode(
        x=alt.X('finish_year:O', title='Year'),
        y=alt.Y('Book Title', title=None)
    )

    return chart

st.title('Book Data')
st.header('Yearly Overview')
# Threshold to be considered a book
min_pages_per_book = st.number_input('Pick number of pages to set as threshold', 0)

# filter by finished books
completed_books = st.session_state.book_data[~st.session_state.book_data['Finish Date'].isnull()]

books_by_year = completed_books[completed_books['Pages'] > min_pages_per_book].groupby('finish_year')['Book Title'].count().sort_values(ascending=False).to_frame().reset_index()



st.text('Number of books read each year')
st.altair_chart(books_by_year_chart(books_by_year))

st.header('Genres')
