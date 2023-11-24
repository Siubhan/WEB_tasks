import sqlite3
from scripts import *
import pandas as pd

if __name__ == '__main__':
    connect = sqlite3.connect('booking.db')
    cursor = connect.cursor()
    # cursor.execute(script_1)
    # cursor.execute(script_2)
    # cursor.execute(script_3)
    # cursor.executescript(script_4)
    # cursor.execute(script_5)
    # print(cursor.fetchall())

    # connect.commit()
    # connect.close()


    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('max_colwidth', None)
    df = pd.read_sql(script_2, connect)
    print(df)
