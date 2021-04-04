import PySimpleGUI as sg
from classes import *
import random

MIN_GEN_CNT, MAX_GEN_CNT = 4, 8

books = [Book(['Михаил Булгаков'], 'Мастер и Маргарита', 'Юнацтва Минск', 1966, 670, 'Художественная лит-ра', 500),
         Book(['Александр Дюма'], 'Граф Монте-Кристо', 'Азбука-Аттикус', 2019, 1300, 'Художественная лит-ра', 600),
         Book(['Эрих Мария Ремарк'], 'Время жить и время умирать', 'АСТ', 2020, 384, 'Художественная лит-ра', 300),
         Book(['Джордж Оруэлл'], '1984', 'АСТ', 2016, 380, 'Художественная лит-ра', 450),
         Book(['Теодор Драйзер'], 'Американская трагедия', 'АСТ', 2021, 960, 'Художественная лит-ра', 400),
         Book(['Ильин В.А.', 'Садовничий В.А.', 'Сендов Бл.Х.'], 'Математический анализ', 'Юрайт', 2019, 648, 'Учебная лит-ра', 740),
         Book(['Александров Н.В.', 'Яшкин А.Я.'], 'Курс общей физики. Механика', 'Юрайт', 1978, 416, 'Учебная лит-ра', 630),
         Book(['Бьярне Страуструп'], 'Программирование на C++', 'Вильямс', 2018, 1328, 'Учебная лит-ра', 1500), ]

DEFAULT_FONT = ('Arial', 10)
left_col1 = [
    [sg.Text('Simulation period (days)', font=DEFAULT_FONT), sg.InputText('15', font=DEFAULT_FONT, size=(3, 1))],
    [sg.Text('Simulation step (days)', font=DEFAULT_FONT), sg.InputText('3', font=DEFAULT_FONT, size=(3, 1))],
    [sg.Text('Delivery range (days)', font=DEFAULT_FONT), sg.InputText('2-4', font=DEFAULT_FONT, size=(3, 1))],
    [sg.Text('Margin (%)', font=DEFAULT_FONT), sg.InputText('20', font=DEFAULT_FONT, size=(3, 1))],
    [sg.Text('Margin for new books (%)', font=DEFAULT_FONT), sg.InputText('30', font=DEFAULT_FONT, size=(3, 1))],
    [sg.Text('Min count for order book', font=DEFAULT_FONT), sg.InputText('5', font=DEFAULT_FONT, size=(3, 1))],
    [sg.Button('Start', font=DEFAULT_FONT), sg.Button('Exit', font=DEFAULT_FONT)]]
cnt_parameters = len(left_col1) - 1  # -1  -- row with buttons
headers = [sg.Text('Launch parameters', font=DEFAULT_FONT, size=(33, 1), justification='c'),
           sg.Text('Starting counts of each book', font=DEFAULT_FONT, size=(90, 1), justification='c')]
right_col1 = []
for book in books:
    text = str(book)
    right_col1.append(
        [sg.Text(text, font=(DEFAULT_FONT[0], DEFAULT_FONT[1] if len(text) < 55 else DEFAULT_FONT[1] - 2)),
         sg.Input(str(random.randint(MIN_GEN_CNT, MAX_GEN_CNT)), font=DEFAULT_FONT, size=(3, 1))])

layout1 = [headers,
           [sg.Column(left_col1, element_justification='r'),
            sg.Column(right_col1, element_justification='r', size=(650, 160), scrollable=True)]]

window1 = sg.Window('Book shop. Input parameters.', layout1)
def create_col(name_col, arg):
    global DEFAULT_FONT
    widths = {'Автор': 40, 'Название': 30, 'Кол-во': 12, 'Покупатель': 20, '#': 2, 'Тематика': 25, 'Издат.': 12,
              'Рейтинг': 14}
    num_rows = 7
    justification = 'l'
    if name_col == 'Ассортимент':  # arg - List[BookCopies]
        headings = ['Автор', 'Название', '#']
        data = [[', '.join(bc.book.authors), bc.book.name, bc.count] for bc in arg]
    elif name_col == 'Текущие заказы' or name_col == 'Выполн. заказы':  # arg - List[Order]
        headings = ['Покупатель', 'Автор', 'Название', '#']
        data = [[orde.customer, '\n'.join([', '.join(bc.book.authors) for bc in orde.cart]),
                 '\n'.join([bc.book.name for bc in orde.cart]), '\n'.join([str(bc.count) for bc in orde.cart])] for orde in arg]
    elif name_col == 'Продажи':  # arg - OrderedDict[(category, cnt)]
        headings = ['Тематика', '#']
        data = [[cat, cnt] for cat, cnt in arg.items()]
    elif name_col == 'Выполн. заявки в издат.':  # arg - List[OrderPublishing]
        headings = ['Издат.', 'Автор', 'Название', '#']
        data = [[orde.publishing, '\n'.join([', '.join(bc.book.authors) for bc in orde.books_copies]),
                 '\n'.join([bc.book.name for bc in orde.books_copies]), '\n'.join([str(bc.count) for bc in orde.books_copies])] for orde in arg]
    elif name_col == 'Топ-10 книг':  # arg - List[Order]
        #топ - 10 книг: книга, рейтинг, кол - во
        headings = ['Автор', 'Название', 'Рейтинг', '#']
        #data =
    else:
        raise ValueError(f"Unexpected name_col = {name_col}")
    col_widths = [widths[head] for head in headings]
    table = sg.Table(values=data, headings=headings,
                     justification=justification,
                     num_rows=num_rows,
                     auto_size_columns=False,
                     font=DEFAULT_FONT,
                     col_widths=col_widths)
    col_assort = [[sg.Text(name_col, justification='c', font=DEFAULT_FONT, size=(sum(col_widths), 1))], [table]]
    return col_assort

window = 1
while True:
    if window == 1:
        event, val = window1.read()
        if event == sg.WIN_CLOSED or event == 'Exit':  # if user closes window or clicks Exit
            break
        elif event == 'Start':
            window = 2
            start_assort = [int(x) for x in val[cnt_parameters:]]
            delivery_range = val[2].split('-')
            delivery_range = tuple([int(delivery_range[0]), int(delivery_range[1])])
            experiment = Experiment(simulation_period=int(val[0]), simulation_step=int(val[1]), books=books,
                                    start_assort=start_assort, delivery_range=delivery_range,
                                    minimum_cnt_for_order=int(val[5]), margin=int(val[3]), margin_new_book=int(val[4]))
            experiment.start()
            window1.hide()
    else:  # i.e. window == 2
        col_assort = create_col('Ассортимент', experiment.book_shop.books)
        col_orders = create_col('Текущие заказы', experiment.book_shop.orders)
        col_stat = create_col('Продажи', experiment.sell_statistic)
        col_done_ord_publ = create_col('Выполн. заявки в издат.', experiment.done_orders_publishing)
        col_done_ord = create_col('Выполн. заказы', experiment.done_orders)
        #col_top10_book = create_col('Топ-10 книг', )
        layout2 = [[sg.Column(col_assort), sg.Column(col_orders), sg.Column(col_stat)],
                   [sg.Column(col_done_ord_publ), sg.Column(col_done_ord)],
                   [sg.Button('Stop', font=DEFAULT_FONT), sg.Button('Exit', font=DEFAULT_FONT)]]
        window2 = sg.Window('Book Shop', layout2)

        event, val = window2.read()
        if event == 'Stop':
            window = 1
            window2.hide()
            window1.un_hide()
        elif event == sg.WIN_CLOSED or event == 'Exit':
            break

window1.close()
