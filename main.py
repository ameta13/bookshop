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
         Book(['Бьярне Страуструп'], 'Программирование на C++', 'Вильямс', 2018, 1328, 'Учебная лит-ра', 1500),]

DEFAULT_FONT = ('Arial', 10)
left_col1 = [[sg.Text('Launch parameters', font=DEFAULT_FONT)],
            [sg.Text('Simulation period (days)', font=DEFAULT_FONT), sg.InputText('15', font=DEFAULT_FONT, size=(3, 1))],
            [sg.Text('Simulation step (days)', font=DEFAULT_FONT), sg.InputText('3', font=DEFAULT_FONT, size=(3, 1))],
            [sg.Text('Delivery range (days)', font=DEFAULT_FONT), sg.InputText('2-4', font=DEFAULT_FONT, size=(3, 1))],
            [sg.Text('Margin (%)', font=DEFAULT_FONT), sg.InputText('20', font=DEFAULT_FONT, size=(3, 1))],
            [sg.Text('Margin for new books (%)', font=DEFAULT_FONT), sg.InputText('30', font=DEFAULT_FONT, size=(3, 1))],
            [sg.Text('Min count for order book', font=DEFAULT_FONT), sg.InputText('5', font=DEFAULT_FONT, size=(3, 1))],
            [sg.Button('Start', font=DEFAULT_FONT), sg.Button('Exit', font=DEFAULT_FONT)]]
cnt_parameters = len(left_col1) - 2  # -2  -- 'Launch parameters' and row with buttons
right_col1 = [[sg.Text('Starting counts of each book',)]]
for book in books:
    text = ', '.join(book.authors) + ': ' + book.name
    right_col1.append([sg.Text(text, font=(DEFAULT_FONT[0], DEFAULT_FONT[1] if len(text) < 55 else DEFAULT_FONT[1]-2)),
                      sg.Input(str(random.randint(MIN_GEN_CNT, MAX_GEN_CNT)), font=DEFAULT_FONT, size=(3, 1))])
layout1 = [[sg.Column(left_col1, element_justification='r'), sg.Column(right_col1, element_justification='r')]]

window1 = sg.Window('Book shop. Input parameters.', layout1)
while True:
    event, val = window1.read()
    if event == sg.WIN_CLOSED or event == 'Exit':  # if user closes window or clicks Exit
        break
    if event == 'Start':
        start_assort = [int(x) for x in val[cnt_parameters:]]
        delivery_range = val[2].split('-')
        delivery_range = tuple([int(delivery_range[0]), int(delivery_range[1])])
        experiment = Experiment(simulation_period=int(val[0]), simulation_step=int(val[1]), books=books,
                                start_assort=start_assort, delivery_range=delivery_range,
                                minimum_cnt_for_order=int(val[5]), margin=int(val[3]), margin_new_book=int(val[4]))
        experiment.start()
        cols_books = [sg.Column([[] for book in books]) ]
        cols_window2 = []
        cols_window2.append([[sg.Text('Ассортимент')],
                             ])
        #window1.hide()
        #layout2 =

window1.close()
