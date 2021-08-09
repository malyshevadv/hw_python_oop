from __future__ import annotations
from typing import Union, Optional
import datetime as dt


class Calculator:
    """The base calcualtor class. Stores records, counts stats"""

    def __init__(self, limit: Union[int, float]) -> None:
        self.limit = limit
        self.records = []

    def add_record(self, new_record: Record) -> None:
        self.records.append(new_record)

    def get_today_stats(self) -> Union[int, float]:
        cutoff_date = dt.date.today()
        return sum(rec.amount for rec in self.records
                   if rec.date == cutoff_date)

    def get_week_stats(self) -> Union[int, float]:
        current_date = dt.date.today()
        cutoff_date = current_date - dt.timedelta(days=7)

        return sum(rec.amount for rec in self.records
                   if cutoff_date <= rec.date <= current_date)

    def get_remainder(self) -> Union[int, float]:
        amount_spent = self.get_today_stats()
        return self.limit - amount_spent


class Record:
    def __init__(self, amount: Union[int, float], *kwargs,
                 comment: str = '',
                 date: Optional[str] = None) -> None:
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class CashCalculator(Calculator):
    """Cash calcualtor, derived from calcualtor.
       Can count cash. Lives sometime before
       Sept 2014 based on the exchange rates.
    """

    USD_RATE = 33.32
    EURO_RATE = 50.45
    currencies = {'rub': ('руб', 1),
                  'usd': ('USD', USD_RATE),
                  'eur': ('Euro', EURO_RATE)}

    def get_today_cash_remained(self, currency: str) -> str:
        difference = self.get_remainder()
        if difference == 0:
            return 'Денег нет, держись'

        currency_name, currency_rate = CashCalculator.currencies[currency]

        difference = round(difference / currency_rate, 2)

        if difference > 0:
            return f'На сегодня осталось {difference} {currency_name}'
        else:
            difference = abs(difference)
            return ('Денег нет, держись: '
                    f'твой долг - {difference} {currency_name}')


class CaloriesCalculator(Calculator):
    """Calories calcualtor, derived from calcualtor.
       Can count calories
    """

    def get_calories_remained(self) -> str:
        difference = self.get_remainder()

        if (difference > 0):
            return ('Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более {difference} кКал')
        else:
            return 'Хватит есть!'
