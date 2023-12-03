from jinja2 import Template
import sqlite3
from library_model import get_table

if __name__ == '__main__':
    # устанавливаем соединение с базой данных (базу данных взять из ЛР 1)
    conn = sqlite3.connect("library.sqlite")

    res = conn.execute("SELECT name FROM sqlite_master WHERE type='table' and name <> 'sqlite_sequence';")
    df_tables = []
    names = []
    for name in res:
        df_tables.append(get_table(conn, name[0]))
        names.append(name[0])
    # закрываем соединение с базой
    conn.close()
    # открываем шаблон из файла library_templ.html и читаем информацию
    with open('library_template.html', 'r', encoding='utf-8-sig') as template_file:
        html = template_file.read()

    # создаем объект-шаблон
    template = Template(html)

    # генерируем результат на основе шаблона
    result_html = template.render(
        tables=names,
        relations=df_tables,
        len=len
    )

    # создаем файл для HTML-страницы
    with open('library.html', 'w', encoding='utf-8-sig') as file:
        file.write(result_html)
