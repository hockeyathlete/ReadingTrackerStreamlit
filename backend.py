import pandas as pd
import psycopg2


def load_data(user):
    # connect to database
    conn = psycopg2.connect(
        "dbname='reading_tracker' user='postgres' password='postgres123' host='localhost' port='5432'")
    books = pd.read_sql('SELECT * FROM books', conn)
    log = pd.read_sql('SELECT * FROM logs', conn)
    # Load Data
    # if user == 'Alan':
    # sheet_id = '1lQQliuMCJPLcfn3CzaK4aU6-Ro3wkMJ1Ghqa8vdJ1ho'
    # elif user == 'Michaels':
    #     sheet_id = '1P6fvMYKev5RS_M3ClTb-KiLPU-HOKplO-3grupqCdNI'
    # elif user == 'Jeff':
    #     sheet_id = '1hJLYGq46kB_Z15HGLy_kCbyB4DLYu2esra_Gl_bFPOU'
    # book_tracker = 'Book%20Tracker'
    # book_tracker_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={book_tracker}'
    # reading_log = 'Reading%20Log'
    # reading_log_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={reading_log}'
    # log = pd.read_csv(reading_log_url)
    ebook_normalizer = 0.89

    # Preprocess Book Data
    books['start_date'] = pd.to_datetime(books['start_date'])
    books['finish_date'] = pd.to_datetime(books['finish_date'])
    books.loc[~books['finish_date'].isnull(), 'finish_year'] = pd.to_datetime(books['finish_date']).dt.year
    books.loc[~books['finish_date'].isnull(), 'month_year'] = pd.to_datetime(books['finish_date']).dt.to_period('M').astype(str)
    books['days_to_read'] = (books['finish_date']-books['start_date']).dt.days + 1
    books['pages_per_day'] = (books['pages']/books['days_to_read']).round(0)
    books.loc[books['format'] == 'Book', 'pages_norm'] = books['pages']
    books.loc[books['format'] == 'eBook', 'pages_norm'] = round(books['pages'] * ebook_normalizer)
    books.loc[books['format'] == 'Audiobook', 'pages_norm'] = 0

    # Preprocess Log Data
    log['date'] = pd.to_datetime(log['date'])
    log['month_year'] = pd.to_datetime(log['date']).dt.to_period('M').astype(str)
    log['year'] = pd.DatetimeIndex(log['date']).year
    log['weekday'] = pd.DatetimeIndex(log['date']).strftime('%A')

    # log.loc[log['format'] == 'Book', 'pages_norm'] = log['Pages Read']
    # log.loc[log['format'] == 'eBook', 'pages_norm'] = round(log['Pages Read'] * ebook_normalizer)
    # log.loc[log['format'] == 'Audiobook', 'pages_norm'] = 0

    return books, log
