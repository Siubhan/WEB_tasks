from jinja2 import Template, Environment, FileSystemLoader

if __name__ == '__main__':
    with open('task_1.html', 'r', encoding='utf-8-sig') as template_file:
        html = template_file.read()

    template = Template(html)
    result_html = template.render(name="color", dictonary={1: "синий", 2: "зеленый", 3: "красный"}, values=[2, 3])

    with open('result.html', 'w', encoding='utf-8-sig') as file:
        file.write(result_html)

    with open('task_2.html', 'r', encoding='utf-8-sig') as template_file:
        html = template_file.read()

    # macros in another file
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('task_2.html')
    books = [
        {"title": "Мастер и Маргарита",
         "author": "Булгаков М.А.",
         "price": 581.50},
        {"title": "Белая гвардия",
         "author": "Булгаков М.А.",
         "price": 600.00},
        {"title": "Война и мир",
         "author": "Толстой Л.Н.",
         "price": 899.99},
        {"title": "Анна Каренина",
         "author": "Толстой Л.Н.",
         "price": 450.10},
        {"title": "Игрок",
         "author": "Достоевский Ф.М.",
         "price": 234.55}
    ]

    # In jinja2 indexing starts with 1
    # (e.g. Мастер и Маргарита is the first record of list, so it's not included)
    # ! In macros STRICT COMPARSION (first < CURRENT < last)
    result_html = template.render(cards=books, first=0, last=len(books) + 1)

    with open('result_2.html', 'w', encoding='utf-8-sig') as file:
        file.write(result_html)
