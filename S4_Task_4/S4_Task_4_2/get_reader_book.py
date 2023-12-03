from jinja2 import Template
import sqlite3
from reader_book_model import get_reader, get_book_reader

if __name__ == '__main__':
    # задаем id читателя, для которого формируем страницу
    reader_id = 3
    # устанавливаем соединение с базой данных
    conn = sqlite3.connect("library.sqlite")

    # выбираем записи о том, какие книги брал читатель с параметром reader_id
    # столбцы назвать Название, Авторы, Дата_выдачи, Дата_сдачи
    df_book_reader = get_book_reader(conn, reader_id)

    # выбираем записи из таблицы reader для формирования поля со списком
    df_reader = get_reader(conn)
    # закрываем соединение с базой
    # print(df_book_reader)
    conn.close()
    # открываем файл reader_book_templ.html и читаем шаблон
    with open('reader_book_template.html', 'r', encoding='utf-8-sig') as template_file:
        html = template_file.read()

    # создаем объект-шаблон
    template = Template(html)

    # генерируем результат на основе шаблона
    result_html = template.render(
        reader_id=reader_id,
        combo_box=df_reader,
        book_reader=df_book_reader,
        len=len)

    # создаем файл для HTML-страницы
    with open('reader_book.html', 'w', encoding='utf-8-sig') as file:
        file.write(result_html)
