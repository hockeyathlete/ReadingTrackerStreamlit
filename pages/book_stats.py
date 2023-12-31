import pandas as pd
import altair as alt
import streamlit as st
import numpy as np


def books_by_year_chart(books_by_year_data):
    chart = alt.Chart(books_by_year_data, title='Books by Year').mark_bar().encode(
        x=alt.X('finish_year:O', title='Year'),
        y=alt.Y('Book Title', title=None)
    )

    return chart


def books_by_month_chart(books_by_month_data):
    chart = alt.Chart(books_by_month_data, title='Books by Month').mark_bar().encode(
        x=alt.X('month_year:O', title='Month'),
        y=alt.Y('Book Title', title=None)
    )

    return chart


st.title('Book Data')
# Threshold to be considered a book
min_pages_per_book = st.number_input('Pick number of pages to set as threshold', 0)

st.header('Yearly Overview')
# filter by finished books (must meet minimum pages threshold to count)
completed_books = st.session_state.book_data[(~st.session_state.book_data['Finish Date'].isnull()) & (st.session_state.book_data['Pages'] > min_pages_per_book)]

books_by_year = completed_books.groupby('finish_year')[
    'Book Title'].count().sort_values(ascending=False).to_frame().reset_index()

st.text('Number of books read each year')
st.altair_chart(books_by_year_chart(books_by_year))

st.header('Monthly Review')
# add selection for year to review. Sort the available years in the data.
# Using list comprehesion, turn all the values into ints because otherwise it adds a decimal point. Then reverse the
# order of the list to have the most recent year first (this can't be done with the np.sort()
years = np.sort(completed_books['finish_year'].unique())
year = st.selectbox('Pick a year to review', [int(year) for year in years][::-1])

year_data = completed_books[completed_books['finish_year'] == year]
books_by_month = year_data.groupby('month_year')['Book Title'].count().sort_values(
    ascending=False).to_frame().reset_index()

st.altair_chart(books_by_month_chart(books_by_month))
st.header('Genres')
