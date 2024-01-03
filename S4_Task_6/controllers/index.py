from app import app
from flask import render_template, request, session
# import sqlite3
from utils import get_db_connection
from models.index_model import get_reader, get_book_reader, get_new_reader, return_book
from models.search_model import borrow_book


@app.route('/', methods=['get'])
def index():
    conn = get_db_connection()
    # нажата кнопка Найти
    if request.values.get('reader'):
        reader_id = request.values.get('reader_id')
        session['reader_id'] = reader_id

    elif request.values.get('new_reader'):
        new_reader = request.values.get('new_reader')
        session['reader_id'] = get_new_reader(conn, new_reader)

    elif request.values.get('return'):
        book_id = request.values.get('return')
        return_book(conn, book_id)

    elif request.values.get('noselect'):
        a = 1
        # вошли первый раз
    else:
        session['reader_id'] = 1
    df_book_reader = get_book_reader(conn, session['reader_id'])
    df_reader = get_reader(conn)

    html = render_template(
        'index.html',
        reader_id=session['reader_id'],
        combo_box=df_reader,
        book_reader=df_book_reader,
        len=len
    )

    return html
