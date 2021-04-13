import PySimpleGUI as sg
from classes import *
import random

MIN_GEN_CNT, MAX_GEN_CNT = 4, 8
DEFAULT_FONT = ('Arial', 10)


def create_col(name_col, arg):
  global DEFAULT_FONT
  widths = {'Автор': 40, 'Название': 30, 'Кол-во': 12, 'Покупатель': 20, '#': 5, 'Тематика': 25, 'Издат.': 12,
            'Рейтинг': 12, 'Время': 10}
  num_rows = 15
  justification = 'l'
  if name_col == 'Ассортимент':  # arg - List[BookCopies]
    headings = ['Автор', 'Название', '#']
    data = [[', '.join(bc.book.authors), bc.book.name, bc.count] for bc in arg]
  elif name_col == 'Текущие заказы' or name_col == 'Выполн. заказы':  # arg - List[Order]
    headings = ['Покупатель', 'Автор', 'Название']
    if name_col == 'Текущие заказы':
        headings.append('Кол-во')
    else:
        headings.append('#')
    data = [[cust, ', '.join(bc.book.authors), bc.book.name, bc.count]
            for orde in arg for cust, bc in zip([orde.customer] + [''] * (len(orde.cart) - 1), orde.cart)]
  elif name_col == 'Продажи':  # arg - OrderedDict[(category, cnt)]
    headings = ['Тематика', '#']
    data = [[cat, cnt] for cat, cnt in arg.items()]
  elif name_col == 'Выполн. заявки в издат.':  # arg - List[OrderPublishing]
    headings = ['Издат.', 'Автор', 'Название', '#']
    data = [[publ, ', '.join(bc.book.authors), bc.book.name, bc.count]
            for orde in arg for publ, bc in
            zip([orde.publishing] + [''] * (len(orde.books_copies) - 1), orde.books_copies)]
  elif name_col == 'Заявки в издат.':
    headings = ['Издат.', 'Автор', 'Название', 'Время', 'Кол-во']
    data = [[publ, ', '.join(bc.book.authors), bc.book.name, time, bc.count]
            for time, orde in arg for publ, bc in
            zip([orde.publishing] + [''] * (len(orde.books_copies) - 1), orde.books_copies)]
  elif name_col == 'Топ-10 книг':  # arg - List[Order]
    top = 10
    headings = ['Автор', 'Название', 'Рейтинг']
    sort_arg = sorted(arg, key=lambda bc: bc.book.rating, reverse=True)[:top]
    data = [[', '.join(bc.book.authors), bc.book.name, f'{bc.book.rating:.2f}'] for bc in sort_arg]
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


def read_books(path='books.tsv'):
    # Format:
    # Авторы\tНазвание\tИздательство\tГод издания\tКоличество страниц\tКатегория\tСтоимость
    # Авторы -- "Author1; Author2; ..."
    with open(path, 'r') as f:
        rows = f.read().split('\n')[1:]
    rows = [[x if i > 0 else x.split('; ') for i, x in enumerate(r.split('\t'))] for r in rows]
    books = [Book(r[0], r[1], r[2], int(r[3]), int(r[4]), r[5], int(r[6])) for r in rows]
    return books


books = read_books()
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
        col_stat = create_col('Продажи', experiment.sell_statistic_cat)
        col_done_ord_publ = create_col('Выполн. заявки в издат.', experiment.done_orders_publishing)
        col_done_ord = create_col('Выполн. заказы', experiment.done_orders)
        col_top10_book = create_col('Топ-10 книг', experiment.book_shop.books)
        col_ord_publ = create_col('Заявки в издат.', experiment.orders_publishing)

        buttons = [sg.Button('Stop', font=DEFAULT_FONT), sg.Button('Exit', font=DEFAULT_FONT)]
        if experiment.cnt_steps < experiment.simulation_period:
            buttons = [sg.Button('One step', font=DEFAULT_FONT), sg.Button('Run', font=DEFAULT_FONT)] + buttons
        layout2 = [[sg.Column(col_assort), sg.Column(col_top10_book)],
                   [sg.Column(col_orders), sg.Column(col_ord_publ)],
                   [sg.Column(col_done_ord), sg.Column(col_done_ord_publ), sg.Column(col_stat)],
                   buttons]
        window2 = sg.Window(f'Book Shop. Day = {experiment.cnt_steps}', layout2)

        event, val = window2.read()
        if event == 'Run':
          experiment.make_all_steps()
          window2.hide()
        elif event == 'One step':
          experiment.make_step()
          window2.hide()
        elif event == 'Stop':
            window = 1
            window2.hide()
            window1.un_hide()
            del experiment
        elif event == sg.WIN_CLOSED or event == 'Exit':
            break
window1.close()
