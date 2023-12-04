from jinja2 import Template
import sqlite3
from booking_get import get_expected_guests, get_room_type, get_status

if __name__ == '__main__':
    # задаем id типа комнаты, статуса
    status_id = 1
    type_room = 3

    # устанавливаем соединение с базой данных
    conn = sqlite3.connect("booking_1.db")

    df_room_type = get_room_type(conn)
    df_status = get_status(conn)

    df_expect_guest = get_expected_guests(conn, status_id, type_room)

    conn.close()

    # открываем и читаем шаблон
    with open('booking_template.html', 'r', encoding='utf-8-sig') as template_file:
        html = template_file.read()

    # создаем объект-шаблон
    template = Template(html)

    # генерируем результат на основе шаблона
    result_html = template.render(
        status_id=status_id,
        df_status=df_status,
        room_type=type_room,
        df_room_type=df_room_type,
        df_expect_guest=df_expect_guest,
        len=len)

    # создаем файл для HTML-страницы
    with open('booking.html', 'w', encoding='utf-8-sig') as file:
        file.write(result_html)
