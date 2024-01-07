import streamlit as st
from datetime import timedelta, date

st.set_page_config(page_title='Reading Tracker- Top Streaks')


def calculate_longest_streak(daily_log):
    '''this function is modified from https://joshdevlin.com/blog/calculate-streaks-in-pandas/'''
    data = daily_log['Date'].to_frame()
    data['streak_id'] = data.Date.ne(daily_log['Date'].shift() + timedelta(days=1)).cumsum()
    data['streak'] = data.groupby('streak_id').cumcount() + 1
    best_streak = data['streak'].max()
    best_streak_index = data['streak'].idxmax()
    active_date = data['Date'][best_streak_index]
    if active_date.date() == date.today() - timedelta(days=1):
        active = 'Active'
    else:
        active = 'Not Active'
    return best_streak, active, active_date.strftime("%m/%d/%Y")


daily_pages = st.session_state.log_data.groupby('Date', as_index=False)['Pages Read'].sum()
page_counts = (0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 150, 200)
days = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
streaks = dict(zip(page_counts, days))
for pages in page_counts:
    page_count_log = daily_pages[daily_pages['Pages Read'] > pages]
    if page_count_log.shape[0] > 0:
        streaks[pages] = calculate_longest_streak(page_count_log)
    else:
        streaks[pages] = 0, 'Not Active', 'N/A'

st.title('Top Streaks')
for pages, days in streaks.items():
    st.text(f'Days in a row (>{pages} pages): {days[0]} | {days[1]} | {days[2]}')
