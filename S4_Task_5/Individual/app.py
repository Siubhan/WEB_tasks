from flask import Flask, render_template, request
from math import acos, sqrt, degrees
from numpy import cross, array

app = Flask(__name__)


#  Разработать калькулятор для реализации операций c двумя векторами длиной n.
#  Калькулятор должен вычислять:
#
#  **   модуль векторов;
#  **   угол между векторами;
#  **   векторное произведение;
#  **   разность.
#
# Калькулятор должен включать:
#
#  **   числовое поле для ввода размера векторов и кнопку Показать;
#  **   поля для ввода каждого элемента векторов;
#  **   группу переключателей (checkbox) для выбора одной или нескольких операций;
#  **  кнопки Вычислить и Очистить.
#
# ** В начальный момент времени на странице должно отобразиться поле для ввода размера векторов со значением 2,
# ** по 4 числовых поля для ввода элементов векторов,
# ** а также реализуемые операции, перечисленные в группе переключателей.
#
# После ввода пользователем нового размера матрицы и клику по кнопке
# Показать, на страницу должно быть выведено необходимое количество полей для ввода элементов векторов;
#
# После ввода пользователем элементов векторов,
# выбора операций и клику по кнопке Вычислить,
# на той же странице вывести результаты расчетов.
# Вся введенная пользователем информация в формах после обновления страницы должна сохраняться.
#
# При клике на кнопку Очистить – очистить поля для ввода элементов векторов.

@app.route('/', methods=['GET'])
def index():
    req = bool(request.values)
    size = request.values.get('size', 2, int)
    result = []

    vector_a = [0] * size
    vector_b = [0] * size
    options = request.values.getlist('options')

    if options:
        vector_a = request.values.getlist('a', int)
        vector_b = request.values.getlist('b', int)

        if 'vect' in options:
            vect_mult = cross(array(vector_a), array(vector_b))
            result.append(f'Векторное произведение: {vect_mult}\n')

        if 'substraction' in options:
            vect_sub = array(vector_a) - array(vector_b)
            result.append(f'Разность: {vect_sub}\n')

        if 'angle' in options:
            m = sum([a * b for a, b in [(vector_a[i], vector_b[i]) for i in range(size)]])
            mod_a = sqrt(sum([i * i for i in [vector_a[j] for j in range(size)]]))
            mod_b = sqrt(sum([i * i for i in [vector_b[j] for j in range(size)]]))

            result.append(f'Угол между векторами: {degrees(acos(m / (mod_a * mod_b))):.2f}\n')

        if 'mod' in options:
            mod_a = sqrt(sum([i * i for i in [vector_a[j] for j in range(size)]]))
            mod_b = sqrt(sum([i * i for i in [vector_b[j] for j in range(size)]]))

            result.append(f'Модуль вектора А: {mod_a:.2f}')
            result.append(f'Модуль вектора В: {mod_b:.2f}\n')
    # options = zip(range(len(options)), options)
    # options = dict(options)
    html = render_template(
        'index.html',
        size=size,
        A=vector_a,
        B=vector_b,
        result=result,
        options=options,
    )
    return html


