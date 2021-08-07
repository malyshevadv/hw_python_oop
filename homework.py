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

    def get_today_stats(self) ->  Union[int, float]:
        cutoff_date = dt.date.today()
        total = 0
        for rec in self.records:
            if (rec.date == cutoff_date):
                total += rec.amount
        return total

    def get_week_stats(self) ->  Union[int, float]:
        current_date = dt.date.today()
        cutoff_date = dt.date.today() - dt.timedelta(days=7)
        total = 0
        for rec in self.records:
            if (rec.date >= cutoff_date and rec.date <= current_date):
                total += rec.amount
        return total

class Record:
    def __init__(self, amount: Union[int, float], *kwargs,
                 comment: str = '', 
                 date: Optional[str] = None) -> None:
        self.amount = amount
        self.comment = comment
        if (date == None):
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class CashCalculator(Calculator):
    """Cash calcualtor, derived from calcualtor. 
       Can count cash. Lives sometime before Sept 2014 based on the exchange rates
    """

    USD_RATE = 33.32
    EURO_RATE = 50.45
    cur_dict = {'rub':'руб', 'usd': 'USD', 'eur': 'Euro'}

    def get_today_cash_remained(self, currency: str) -> str:
        money_spent = self.get_today_stats()
        difference = self.limit - money_spent

        str_cur_name = CashCalculator.cur_dict[currency]
        if (currency == 'usd'):
            difference /= CashCalculator.USD_RATE
        if (currency == 'eur'):
            difference /= CashCalculator.EURO_RATE

        difference = round(difference, 2)
        if (difference > 0):
            result = f'На сегодня осталось {difference} {str_cur_name}'
        elif (difference == 0):
            result = f'Денег нет, держись'
        else:
            difference = abs(difference)
            result = f'Денег нет, держись: твой долг - {difference} {str_cur_name}'
        
        return result
        


class CaloriesCalculator(Calculator):
    """Calories calcualtor, derived from calcualtor. Can count calories"""
    
    def get_calories_remained(self) -> str:
        kkal_eaten = self.get_today_stats()
        difference = self.limit - kkal_eaten

        if (difference > 0):        
            result = (f'Сегодня можно съесть что-нибудь ещё, '
                      f'но с общей калорийностью не более {difference} кКал')
        else:
            result = 'Хватит есть!'

        return result


cash_calculator = CashCalculator(1000)

# дата в параметрах не указана,
# так что по умолчанию к записи
# должна автоматически добавиться сегодняшняя дата
cash_calculator.add_record(Record(amount=145, comment='кофе'))
# и к этой записи тоже дата должна добавиться автоматически
cash_calculator.add_record(Record(amount=300, comment='Серёге за обед'))
# а тут пользователь указал дату, сохраняем её
cash_calculator.add_record(Record(amount=3000,
                                  comment='бар в Танин др',
                                  date='08.11.2019'))
cash_calculator.add_record(Record(amount=3000,
                                  comment='бар в Танин др',
                                  date='05.08.2021'))

print(cash_calculator.get_week_stats())
# должно напечататься
# На сегодня осталось 555 руб 