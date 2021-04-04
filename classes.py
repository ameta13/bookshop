import random
from collections import OrderedDict, defaultdict
from typing import List, Tuple

CURRENT_YEAR = 2021

# TODO: добавить вычисление рейтинга книги

class Book:
    def __init__(self, authors: List[str], name: str, publishing: str, year: int, pages: int, category: str,
                 price: float, margin: int = 0, rating: float = 0):
        self.authors = authors
        self.name = name
        self.publishing = publishing
        self.year = year
        self.pages = pages
        self.price = price
        self.margin = margin
        self.rating = rating
        self.category = category

    def __str__(self):
        return ', '.join(self.authors) + ': ' + self.name


class BookCopies:
    def __init__(self, book: Book, count: int):
        self.book = book
        self.count = count


class Order:
    def __init__(self, customer: str, contact: str, cart: List[BookCopies]):
        self.customer = customer
        self.contact = contact
        self.cart = cart
        self.remain_cart = [i for i in range(len(cart))]


class OrderPublising:
    def __init__(self, publishing: str, books_copies: List[BookCopies]):
        self.publishing = publishing
        self.books_copies = books_copies
        return


class Randomizer:
    def __init__(self, delivery_range: Tuple[int], cnt_books: int, books: List[Book]):
        self.delivery_range = delivery_range
        self.cnt_books = cnt_books  # количество различных книг
        self.books = books
        self.max_diff_book = cnt_books // 2  # максимальное количество различных книг, которое может быть в одном заказе
        self.max_copies = 4  # максимальное количество экземпляров каждой книги в одном заказе
        self.customer_n_contact = [('Smith', 'smith123@gmail.com'),
                                   ('Williams', '+7(926)471-32-32'),
                                   ('Jones', 'baby.jones@duckduck.com'),
                                   ('Brown', 'chrisbrown@msu.ru'),
                                   ('Davis', '+1(309)492-18-27'),
                                   ('Miller', 'ilovejob@miller.com'),
                                   ('Wilson', '+1(778)123-45-67'),
                                   ('Moore', 'moore@more.tv'),
                                   ('Taylor', 'bestsinger@gmail.com'),
                                   ('Scott', 'scotttt@yahoo.com'),]
        self.min_cnt_order = 1  # минимальное кол-во заказов за один шаг
        self.max_cnt_order = 5  # максимальное кол-во заказов за один шаг
        return

    def rand_delivery_time(self) -> int:
        return random.randint(self.delivery_range[0], self.delivery_range[1])

    def rand_cnt_book_in_order(self) -> int:
        # случайное количество разных книг в заказе
        return random.randint(1, self.max_diff_book)

    def rand_cnt_copies(self) -> int:
        # случайное количество копий для книги в заказе
        return random.randint(1, self.max_copies)

    def rand_book(self) -> int:
        # случайная книга
        return random.randint(0, self.cnt_books - 1)

    def rand_order(self) -> Order:
        cnt = self.rand_cnt_book_in_order()
        order = random.sample(self.books, cnt)
        customer, contact = random.choice(self.customer_n_contact)
        cart = [BookCopies(book, self.rand_cnt_copies()) for book in order]
        return Order(customer, contact, cart)

    def rand_cnt_order(self) -> int:
        return random.randint(self.min_cnt_order, self.max_cnt_order)


class BookShop:
    def __init__(self, books_assort: List[BookCopies], minimum_cnt_for_order: int, margin: int, margin_new_book: int, experiment):
        self.orders = []
        self.books = books_assort
        self.minimum_cnt_for_order = minimum_cnt_for_order
        self.margin = margin
        self.margin_new_book = margin_new_book
        self.experiment = experiment  # так ли надо?
        self.auth_name2idx_book = {str(bc.book): idx for idx, bc in enumerate(self.books)}
        self.min_cnt_order_book = 0  # сколько раз заказали наименее популярную книгу (с наименьшим числом заказов)
        self.max_cnt_order_book = -1  #сколько раз заказали наиболее популярную книгу (с наибольшим числом заказов)
        return

    def receive_order(self, new_order: Order):
        # TODO: добавить вычисление рейтинга книги
        self.orders.append(new_order)
        return

    def try_complete_orders(self):
        """
        если из заказа в наличии есть книга в нужном кол-ве, то она откладывается из ассортимента (выкидываем из remain_cart)
            И составляется заказ в издательство на self.minimum_cnt_for_order, если после вычитания у нас осталось "< minimum_cnt_for_order" книг
        Если из заказа нет нужного кол-ва определенной книги (надо N книг), то в издательство заказывается N книг
        """
        order_publ = {}
        for order in self.orders:
            for i, in order.remain_cart:
                bc = order.cart[i]
                idx_book_in_assort = self.auth_name2idx_book[str(bc.book)]
                book = self.books[idx_book_in_assort].book
                if bc.count <= self.books[idx_book_in_assort].count:
                    self.books[idx_book_in_assort].count -= bc.count
                    order.remain_cart.pop(i)
                    cnt_in_assort = self.books[idx_book_in_assort].count
                    if cnt_in_assort < self.minimum_cnt_for_order:
                        if book.publishing not in order_publ:
                            order_publ[book.publishing] = defaultdict(int)
                        order_publ[book.publishing][book] += self.minimum_cnt_for_order
                else:
                    if book.publishing not in order_publ:
                        order_publ[book.publishing] = defaultdict(int)
                    order_publ[book.publishing][book] += bc.count
            if len(order.remain_cart) == 0:
                self.experiment.update_done_order(order)
        for publ, orders_to_publ in order_publ.items():
            ord_publ = OrderPublising(publ, [BookCopies(book, cnt) for book, cnt in orders_to_publ.items()])
            self.experiment.add_order_publishing(ord_publ)
        return

    def get_books_from_publishing(self, orders: List[OrderPublising]):
        new_books_copies = [book_copies for order in orders for book_copies in order.books_copies]
        for new_book_copies in new_books_copies:
            id_book = [id for id, book_copies in enumerate(self.books) if book_copies.book == new_book_copies.book]
            assert len(id_book) == 1, f'BookShop:: get_books_from_publishing(): found {len(id_book)} identical book!'
            id_book = id_book[0]
            self.books[id_book].count += new_book_copies.count


class Experiment:
    def __init__(self, simulation_period: int, simulation_step: int, books: List[Book], start_assort: List[int],
                 delivery_range: Tuple[int], minimum_cnt_for_order: int, margin: int, margin_new_book: int):
        self.simulation_period = simulation_period
        self.simulation_step = simulation_step
        assert len(delivery_range) == 2, f"Experiment:: len(delivery_range) must be equal 2!"
        self.delivery_range = delivery_range
        self.minimum_cnt_for_order = minimum_cnt_for_order
        self.margin = margin
        self.margin_new_book = margin_new_book
        assert len(start_assort) == len(books), f"Wrong length of 'start_assort' = {len(start_assort)}, expected: {len(books)}"
        for book in books:
            book.margin = margin_new_book if book.year == CURRENT_YEAR else margin
        self.start_book_assort = [BookCopies(book, cnt) for book, cnt in zip(books, start_assort)]
        self.orders_publishing = []
        self.done_orders = []
        self.done_orders_publishing = []
        self.randomizer = Randomizer(delivery_range, len(books), books)
        self.book_shop = None  # сам магазин (класс BookShop)

        categories = set([b.category for b in books])
        sell_statistic = {cat: 0 for cat in categories}
        self.sell_statistic = OrderedDict(sorted(sell_statistic.items()))
        self.cnt_steps = 0
        return

    def start(self):
        self.book_shop = BookShop(self.start_book_assort, self.minimum_cnt_for_order, self.margin, self.margin_new_book, self)
        # дописать

    def make_one_step(self):
        cnt_orders = self.randomizer.rand_cnt_order()
        for i in range(cnt_orders):
            self.create_order()
        self.check_orders_publising()
        self.book_shop.try_complete_orders()
        return

    def make_step(self):
        for i in range(self.simulation_step):
            self.make_one_step()
        self.cnt_steps += self.simulation_step

    def make_all_steps(self):
        while self.cnt_steps < self.simulation_period:
            self.make_step()

    def create_order(self):
        new_order = self.randomizer.rand_order()
        self.book_shop.receive_order(new_order)
        return

    def add_order_publishing(self, order: OrderPublising):
        delivery_time = self.randomizer.rand_delivery_time()
        self.orders_publishing.append((delivery_time, order))
        return

    def check_orders_publising(self):
        done_orders = [order for time, order in self.orders_publishing if time == 0]
        if len(done_orders) > 0:
            self.done_orders_publishing += done_orders
            self.orders_publishing = [x for x in self.orders_publishing if x[0] > 0]
            self.book_shop.get_books_from_publishing(done_orders)
        return

    def update_done_order(self, new_done_order: Order):
        self.done_orders.append(new_done_order)
        for bc in new_done_order.cart:
            self.sell_statistic[bc.book.category] += bc.count
        return
