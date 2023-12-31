import pandas as pd
import numpy as np
from datetime import timedelta, date

# Load Data
sheet_id = '1lQQliuMCJPLcfn3CzaK4aU6-Ro3wkMJ1Ghqa8vdJ1ho'
book_tracker = 'Book%20Tracker'
book_tracker_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={book_tracker}'
reading_log = 'Reading%20Log'
reading_log_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={reading_log}'
books = pd.read_csv(book_tracker_url)
log = pd.read_csv(reading_log_url)
ebook_normalizer = 0.89

# Book Data
books['Start Date'] = pd.to_datetime(books['Start Date'])
books['Finish Date'] = pd.to_datetime(books['Finish Date'])

books.loc[books['Format'] == 'Book', 'pages_norm'] = books['Pages']
books.loc[books['Format'] == 'eBook', 'pages_norm'] = round(books['Pages']*ebook_normalizer)
books.loc[books['Format'] == 'Audiobook', 'pages_norm'] = 0