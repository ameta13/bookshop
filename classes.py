import random
from typing import List, Tuple

CURRENT_YEAR = 2021


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

class BookCopies:
    def __init__(self, book: Book, count: int):
        self.book = book
        self.count = count

class Order:
    def __init__(self, customer: str, contact: str, cart: List[BookCopies]):
        self.customer = customer
        self.contact = contact
        self.cart = cart

class OrderPublising:
    def __init__(self, books_copies: List[BookCopies]):
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
        return

    def rand_delivery_time(self):
        return random.randint(self.delivery_range[0], self.delivery_range[1])

    def rand_cnt_book_in_order(self):
        # случайное количество разных книг в заказе
        return random.randint(1, self.max_diff_book)

    def rand_cnt_copies(self):
        # случайное количество копий для книги в заказе
        return random.randint(1, self.max_copies)

    def rand_book(self):
        # случайная книга
        return random.randint(0, self.cnt_books - 1)

    def rand_order(self) -> List[BookCopies]:
        cnt = self.rand_cnt_book_in_order()
        order = random.sample(self.books, cnt)
        customer, contact = random.choice(self.customer_n_contact)
        cart = [BookCopies(book, self.rand_cnt_copies()) for book in order]
        return Order(customer, contact, cart)


class BookShop:
    def __init__(self, start_assort: List[BookCopies], minimum_cnt_for_order: int, margin: int, margin_new_book: int, experiment):
        self.orders = []
        self.books = start_assort
        self.minimum_cnt_for_order = minimum_cnt_for_order
        self.margin = margin
        self.margin_new_book = margin_new_book
        self.experiment = experiment  # так ли надо?
        return

    def receive_order(self, new_order: Order):
        pass

    def create_order_publishing(self, books_copies: BookCopies):
        pass

    def try_complete_orders(self):
        # можно ли частично выполнять заказы? Или сначала в магазине должны собраться все книги и только потом сразу все книги покупатель купит?
        for order in self.orders:
            pass
        # используем self.experiment.update_done_orders_publishing и self.experiment.update_done_orders

    def get_books_from_publishing(self, orders: OrderPublising):
        new_books_copies = [book_copies for order in orders for book_copies in order.books_copies]
        for new_book_copies in new_books_copies:
            id_book = [id for id, book_copies in enumerate(self.books) if book_copies.book == new_book_copies.book]
            assert len(id_book) == 1, f'BookShop:: get_books_from_publishing(): found {len(id_book)} identical book!'
            id_book = id_book[0]
            self.books[id_book].count += new_book_copies.count
        self.try_complete_orders()

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
        self.start_assort = [BookCopies(book, cnt) for book, cnt in zip(books, start_assort)]
        self.orders_publishing = []
        self.done_orders = []
        self.done_orders_publishing = []
        self.randomizer = Randomizer(delivery_range, len(books), books)
        self.book_shop = None  # сам магазин (класс BookShop)
        return

    def start(self):
        self.book_shop = BookShop(self.start_assort, self.minimum_cnt_for_order, self.margin, self.margin_new_book, self)
        # дописать

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
        self.done_orders_publishing += done_orders
        self.book_shop.get_books_from_publishing(done_orders)
        return

    def update_done_orders_publishing(self, new_done_orders_publ):
        self.done_orders_publishing += new_done_orders_publ
        return

    def update_done_orders(self, new_done_orders):
        self.done_orders += new_done_orders
        return
