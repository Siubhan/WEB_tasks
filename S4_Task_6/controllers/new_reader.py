from app import app
from flask import render_template, request, redirect, url_for, session
from models import index_model
from utils import get_db_connection


@app.route('/new_reader', methods=['get'])
def new_reader_get():
    return render_template("new_reader.html")


@app.route('/new_reader_post', methods=['post'])
def new_reader_post():
    conn = get_db_connection()
    reader_name = request.values.get("reader_name")


    inserted_id = index_model.get_new_reader(conn, reader_name)

    session["reader_id"] = inserted_id

    return redirect(url_for("index"))
