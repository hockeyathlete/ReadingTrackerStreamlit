import altair as alt
import streamlit as st
import numpy as np


def pages_per_day_chart(pages_per_day_data):
    base = alt.Chart(pages_per_day_data).mark_bar().encode(
        x=alt.X('month_year', title='Month'),
    )

    chart = alt.hconcat(
        base.encode(y='Pages Read').properties(title='Avg Pages/Day'),
        base.encode(y=alt.Y('pages_norm', title='Pages Read')).properties(title='Avg Pages/Day (Normalized)')
    )
    # chart = base.encode(y='Pages Read')
    return chart


st.title('Page Stats')
with st.expander('How pages are counted across different mediums'):
    st.text('Normalized data means eBooks pages are multiplied by a factor of 0.89 to account \nfor shorter pages')
    st.text('Audiobooks are excluded from this data')

st.header('Pages per Day')
years = np.sort(st.session_state.log_data['year'].unique())
year = st.selectbox('Pick a year to review', [int(year) for year in years][::-1])

pages_per_day = st.session_state.log_data[st.session_state.log_data['year'] == year].groupby('Date').agg(
    {'Pages Read':'sum', 'pages_norm':'sum', 'month_year':'first'}).groupby('month_year')[['Pages Read', 'pages_norm']]\
    .mean().reset_index()

st.altair_chart(pages_per_day_chart(pages_per_day))
