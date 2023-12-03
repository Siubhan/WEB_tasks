import pandas as pd


# Задание - 1
# Для всех номеров, относящихся к типам, названия которых не содержат "люкс",
# и имеющих статус Забронирован в таблице room_booking, вывести информацию
# об их предполагаемом использовании. Для этого указать название номера,
# дату предполагаемого заселения, количество дней проживания.
# Последний столбец назвать Количество_дней. Информацию отсортировать
# сначала по названию номера в алфавитном порядке, потом по возрастанию даты заселения.
#
#
# Пояснение.
#
# Количество дней проживания вычисляется по формуле:
# количество_дней_проживания = дата_выселения - дата_заселения + 1.

def get_expected_guests(conn, status_id=1, type_room=1):
    return pd.read_sql_query(f'''
    SELECT room.room_name, check_in_date,
    CAST((julianday(check_out_date) - julianday(check_in_date) + 1) AS INTEGER) AS 'Count days'
    FROM room_booking INNER JOIN room USING(room_id)
    WHERE status_id = {status_id} AND room.type_room_id = {type_room} ORDER BY room.room_name, check_in_date;
    ''', conn)


def get_room_type(conn):
    return pd.read_sql_query('''SELECT * FROM type_room''', conn)


def get_status(conn):
    return pd.read_sql_query('''SELECT * FROM status''', conn)
