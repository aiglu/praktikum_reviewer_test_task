import datetime as dt

# В целом по всему коду хотелось бы видеть больше комментариев (документации) -
# что это за классы, для чего все эти функции.
class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        # Тернарный оператор if лучше использовать для коротких условий,
        # которые можно записать в одну строку. В данном случае подойдёт обычный if/elif/else.
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        # Record - имя класса, в данном случае надо использовать имя переменной,
        # которое начинается со строчной буквы - record.
        for Record in self.records:
            if Record.date == dt.datetime.now().date():
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            # Расположение по строкам лучше сделать так:
            # if ((today - record.date).days < 7 and
            #         (today - record.date).days >= 0):
            #    week_stats += record.amount
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                # Желательно придерживаться одинакового стиля в однотипных выражениях:
                # или stats = stats + record.amount или stats += record.amount
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    # Комментарий к функции должен быть перед ней, а не рядом.
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        # Переменные лучше называть в соответствии с их смыслом, а не одной буквой.
        x = self.limit - self.get_today_stats()
        if x > 0:
            # Для первой строки необязательно указывать f, потому что в ней не выполняется
            # подстановка данных.
            # Вместо использования бэкслеша лучше заключить строки в скобки.
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        else:
            # А здесь скобки использовать необязательно.
            return('Хватит есть!')


class CashCalculator(Calculator):
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    # Нет необходимости передавать в функцию значения константных курсов валют,
    # их можно просто взять из объекта класса (self).
    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        # Можно не присваивать currency_type = currency, если в условиях
        # ниже везде использовать параметр currency.
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        # В условиях лучше везде использовать параметр currency, а currency_type
        # пусть будет только для вывода в итоговой строке.
        # Тогда можно не присваивать currency_type = currency (на 2 строки выше).
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            # Для чего здесь эта строка? Она совершенно бессмысленна, так как
            # оператор == используется только в условиях, возвращает булево
            # значение - true или false.
            cash_remained == 1.00
            currency_type = 'руб'
        if cash_remained > 0:
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        elif cash_remained < 0:
            # Можно было использовать f-строку, как в функции get_today_cash_remained,
            # для того, чтобы сохранить консистентность.
            # Вместо использования бэкслеша лучше заключить строки в скобки.
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

    # Во-первых, метод родительского класса нужно переопределять, только если нам
    # необходимо поменять его логику.
    # Во-вторых, в вашей реализации данный метод при вызове ничего не вернёт,
    # потому что в нём отсутствует оператор return.
    def get_week_stats(self):
        super().get_week_stats()