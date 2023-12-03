import pandas as pd


def get_reader(conn) -> pd.DataFrame:
    query = "SELECT * FROM reader"
    return pd.read_sql(query, conn)


def get_book_reader(conn, reader_id) -> pd.DataFrame:
    query = f'''SELECT title AS Название, group_concat(author_name) AS Авторы, borrow_date AS Дата_выдачи, return_date AS Дата_сдачи
            FROM book_reader 
            inner join book bk using(book_id)
            inner join book_author ba using(book_id)
            inner join author using(author_id)
            where reader_id = {reader_id} 
            group by title'''
    return pd.read_sql(query, conn)
