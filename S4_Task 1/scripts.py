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

script_1 = '''
SELECT room.room_name, check_in_date,
CAST((julianday(check_out_date) - julianday(check_in_date) + 1) AS INTEGER) AS 'Count days'
FROM room_booking INNER JOIN room USING(room_id)
WHERE status_id = 2 AND room.type_room_id <> 2 ORDER BY room.room_name, check_in_date;
'''

# Задание - 2
# Вывести сводную информацию по гостинице, включающую следующие характеристики:
#
#     Количество гостей - учитывать только тех гостей, которые либо бронировали,
#     либо отменяли бронь, либо проживали в гостинице;
#     Количество номеров - учитывать все номера в гостинице, вне зависимости от того,
#     проживали в нем гости или нет;
#     Сумма за проживание - вычислить общую сумму, которую заплатили гости за проживание в номерах;
#     Количество услуг - учитывать все услуги, которые есть в таблице service;
#     Сумма за услуги - вычислить общую сумму, которую заплатили гости за услуги, предоставляемые гостиницей.
#
# Столбцы назвать Характеристика и Результат, характеристики вывести в том же порядке, как они записаны в задании.

script_2 = '''
    SELECT count(distinct g.guest_name),  
    count(distinct room_booking.room_id) as 'C_room', 
    sum(tr.price*CAST((julianday(check_out_date) - julianday(check_in_date) + 1) AS INTEGER)) AS 'P_booking',
    count(sb.service_id)  AS 'S_service',
    sum(sb.price) AS 'P_service' 
    FROM room_booking inner join guest g USING(guest_id)
    inner join service_booking sb USING(room_booking_id)
    inner join room r USING(room_id) 
    inner join type_room tr USING(type_room_id)
'''

# Задание - 3
# Вывести гостя(ей), который(е) проживали в гостинице за одно заселение
# больше всех по времени. Для каждого из этих гостей указать типы номеров,
# в которых они проживали. Столбцы назвать Номер, Количество_дней, Типы_номеров.
#  Информацию отсортировать по фамилии гостя в алфавитном порядке.

# ! Для третьего запроса использовать табличные выражения (не вложенные запросы)
script_3 = '''
    with count_days(guest_id, room_id, Count_days) AS (
    SELECT guest_id, room_id,
    CAST((julianday(check_out_date) - julianday(check_in_date) + 1) AS INTEGER) AS Count_days
    from room_booking 
    )
    SELECT g.guest_name, r.room_name, tr.type_room_name, Count_days
    from room_booking, count_days inner join room r USING(room_id)
    inner join guest g USING(guest_id)
    inner join type_room tr USING(type_room_id)
    where room_booking.guest_id = count_days.guest_id and room_booking.room_id = count_days.room_id
    group by tr.type_room_name
    having max(Count_days)
    order by g.guest_name
'''

'''
    SELECT g.guest_name, r.room_name, tr.type_room_name, 
    CAST((julianday(check_out_date) - julianday(check_in_date) + 1) AS INTEGER) AS Count_days
    from room_booking inner join room r on r.room_id = room_booking.room_id 
    inner join guest g USING(guest_id)
    inner join type_room tr USING(type_room_id)
    group by tr.type_room_name
    having max(Count_days)
    order by g.guest_name
'''

# Задание - 4
# Гость Астахов И.И., проживающий в номере С-0206 с 2021-01-13, выезжает из гостиницы.
# Перед заселением он внес депозит в размере 15000 рублей, с которого отчислялись суммы
# на оплату заказанных им услуг. Создать таблицу bill, в которую включить отчет
# по депозиту для этого клиента. Отчет включает:
#
#     фамилию гостя, название номера, дату заселения и дату выселения в
#     одном поле (между фамилией гостя и названием номера - пробел,
#     между названием номера и датой заселения - пробел, между датой заселения
#     и датой выселения символ / ), сумма депозита;

#     название услуги, дата (даты) ее получения в одном поле
#     (между названием и датой - пробел, между датами получения услуги, если их несколько,
#     запятая, даты отсортировать в алфавитном порядке),
#     затем вывести общую оплату за эту услугу;
#
#     в последней строке вычислить остаток на депозите (разница депозита и суммы услуг),
#
#     указать Вернуть и оставшуюся от депозита сумму (если деньги на депозите еще есть),
#     Доплатить (если денег на оплату не хватило), Итого (если сумма услуг и депозита совпадает).
#
# Столбцы назвать Вид_платежа и Сумма. Услуги должны быть отсортированы в алфавитном порядке.

script_4 = '''
    with get_services(service_name, service_start_date, sum_price) AS (
    SELECT group_concat(service_name, ', '), group_concat(service_start_date, ', '), sum(price)
    from service_booking 
    inner join room_booking rb using(room_booking_id)
    inner join room r using(room_id)
    inner join guest g using(guest_id)
    inner join service s using(service_id) 
    where g.guest_name = 'Астахов И.И.' and r.room_name = 'С-0206' and rb.check_in_date = '2021-01-13'
    order by s.service_name)
    SELECT 
    guest.guest_name || ' ' || room_booking.check_in_date || '/' || room_booking.check_out_date || ' 15000' as customer_vacation_deposit,
    get_services.service_name, get_services.service_start_date, get_services.sum_price,
    (sum_price - 15000) as debt,
    iif((sum_price - 15000) > 0, 'доплата','погашен') as bill
    from room_booking, get_services
    inner join room r USING(room_id)
    inner join guest using(guest_id)
    inner join room using(room_id)
    where guest.guest_name = 'Астахов И.И.' and r.room_name = 'С-0206' and room_booking.check_in_date = '2021-01-13'
'''

# Задание - 5
# Для каждого гостя посчитать, сколько раз он первым заселялся в любой номер хотя бы один раз.
# Вывести фамилию гостя и посчитанное значение. Последний столбец назвать Количество.
# Информацию отсортировать сначала по убыванию количества, а затем по фамилии гостя в алфавитном порядке.
#
# ! Примечание. Для решения задания № 5 использовать оконные функции.

script_5 = '''
    with cnt as(
    select  *,
    row_number() over (partition by room_id order by check_in_date) rn
    from room_booking 
    ),
    rmCnt as(
    select guest_id, sum(case when rn=1 then 1 else 0 end) cnt
    from cnt group by guest_id
    )
    select guest.guest_name, coalesce(cnt,0) cnt from guest
    left join rmCnt USING(guest_id)
     order by guest_name
'''

