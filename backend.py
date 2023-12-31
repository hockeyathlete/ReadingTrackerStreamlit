import pandas as pd
import numpy as np
from datetime import timedelta, date


def load_data():
    # Load Data
    sheet_id = '1lQQliuMCJPLcfn3CzaK4aU6-Ro3wkMJ1Ghqa8vdJ1ho'
    book_tracker = 'Book%20Tracker'
    book_tracker_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={book_tracker}'
    reading_log = 'Reading%20Log'
    reading_log_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={reading_log}'
    books = pd.read_csv(book_tracker_url)
    log = pd.read_csv(reading_log_url)
    ebook_normalizer = 0.89

    # Preprocess Book Data
    books['Start Date'] = pd.to_datetime(books['Start Date'])
    books['Finish Date'] = pd.to_datetime(books['Finish Date'])
    books.loc[~books['Finish Date'].isnull(), 'finish_year'] = pd.to_datetime(books['Finish Date']).dt.year
    books.loc[~books['Finish Date'].isnull(), 'month_year'] = pd.to_datetime(books['Finish Date']).dt.to_period('M').astype(str)
    books.loc[books['Format'] == 'Book', 'pages_norm'] = books['Pages']
    books.loc[books['Format'] == 'eBook', 'pages_norm'] = round(books['Pages'] * ebook_normalizer)
    books.loc[books['Format'] == 'Audiobook', 'pages_norm'] = 0

    # Preprocess Log Data
    log['Date'] = pd.to_datetime(log['Date'])
    log['month_year'] = pd.to_datetime(log['Date']).dt.to_period('M').astype(str)
    log['year'] = pd.DatetimeIndex(log['Date']).year
    log['weekday'] = pd.DatetimeIndex(log['Date']).strftime('%A')

    log.loc[log['Format'] == 'Book', 'pages_norm'] = log['Pages Read']
    log.loc[log['Format'] == 'eBook', 'pages_norm'] = round(log['Pages Read'] * ebook_normalizer)
    log.loc[log['Format'] == 'Audiobook', 'pages_norm'] = 0

    return books, log
