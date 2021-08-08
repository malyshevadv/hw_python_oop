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
        total = sum(rec.amount for rec in self.records
                    if rec.date == cutoff_date)
        return total

    def get_week_stats(self) -> Union[int, float]:
        current_date = dt.date.today()
        cutoff_date = current_date - dt.timedelta(days=7)
        total = 0
        for rec in self.records:
            if (cutoff_date <= rec.date <= current_date):
                total += rec.amount
        return total

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
        selected_currency = CashCalculator.currencies[currency]

        difference = round(self.get_remainder() / selected_currency[1], 2)

        if (difference > 0):
            result = f'На сегодня осталось {difference} {selected_currency[0]}'
        elif (difference == 0):
            result = 'Денег нет, держись'
        else:
            difference = abs(difference)
            result = ('Денег нет, держись: '
                      f'твой долг - {difference} {selected_currency[0]}')
        return result


class CaloriesCalculator(Calculator):
    """Calories calcualtor, derived from calcualtor.
       Can count calories
    """

    def get_calories_remained(self) -> str:
        difference = self.get_remainder()

        if (difference > 0):
            result = ('Сегодня можно съесть что-нибудь ещё, '
                      f'но с общей калорийностью не более {difference} кКал')
        else:
            result = 'Хватит есть!'

        return result
