import datetime as dt

DATE_FORMAT = "%d.%m.%Y"
TODAY = dt.date.today()
USD_RATE = 85.5
EUR_RATE = 96.4


class Record:
    def __init__(self, amount: int, comment: str, date: str = None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.datetime.now().strftime(DATE_FORMAT)
        else:
            self.date = date


class Calculator:
    def __init__(self, limit: int):
        self.limit = limit
        self.records = []

    def add_record(self, record: Record):
        new_record = {
            "amount": record.amount,
            "comment": record.comment,
            "date": record.date
        }
        self.records.append(new_record)

    def get_today_stats(self) -> float:
        today_amount = 0

        if self.records:
            for record in self.records:
                record_date = dt.datetime.strptime(record["date"], DATE_FORMAT).date()
                if record_date == TODAY:
                    today_amount += record["amount"]

        return today_amount

    def get_week_stats(self):
        one_week_ago = TODAY - dt.timedelta(days=7)
        weekly_amounts = 0

        for record in self.records:
            record_date = dt.datetime.strptime(record["date"], DATE_FORMAT).date()
            if one_week_ago <= record_date <= TODAY:
                weekly_amounts += record["amount"]

        return weekly_amounts


class CashCalculator(Calculator):
    def get_today_stats(self) -> float:
        today_amount_money = super().get_today_stats()
        return f"Сегодня потрачено {today_amount_money} рублей."

    def get_today_cash_remained(self, currency: str) -> str:
        money_spend_today = super().get_today_stats()
        match currency:
            case "rub":
                if self.limit > money_spend_today:
                    diff = self.limit - money_spend_today
                    info = f"На сегодня осталось {diff} рублей."
                elif self.limit < money_spend_today:
                    debt = money_spend_today - self.limit
                    info = f"Денег нет, держись! Твой долг {debt} рублей."
                else:
                    info = "Денег нет, держись!"
            case "usd":
                if self.limit > money_spend_today:
                    diff = (self.limit - money_spend_today) / USD_RATE
                    rounded_diff = round(diff, 2)
                    info = f"На сегодня осталось {rounded_diff} долларов."
                elif self.limit < money_spend_today:
                    debt = (money_spend_today - self.limit) / USD_RATE
                    rounded_debt = round(debt, 2)
                    info = f"Денег нет, держись! Твой долг {rounded_debt} долларов."
                else:
                    info = "Денег нет, держись!"
            case "eur":
                if self.limit > money_spend_today:
                    diff = (self.limit - money_spend_today) / EUR_RATE
                    rounded_diff = round(diff, 2)
                    info = f"На сегодня осталось {rounded_diff} евро."
                elif self.limit < money_spend_today:
                    debt = (money_spend_today - self.limit) / EUR_RATE
                    rounded_debt = round(debt, 2)
                    info = f"Денег нет, держись! Твой долг {rounded_debt} евро."
                else:
                    info = "Денег нет, держись!"        
        return info

    def get_week_stats(self):
        money_spend_last_week = super().get_week_stats()
        return f"За последнюю неделю было потрачено {money_spend_last_week} руб."


class CaloriesCalculator(Calculator):
    def get_today_stats(self) -> float:
        today_amount_calories = super().get_today_stats()
        return f"Сегодня получено {today_amount_calories} кКал"

    def get_calories_remained(self):
        calories_spend_today = super().get_today_stats()
        if self.limit > calories_spend_today:
            diff = self.limit - calories_spend_today
            info = f"Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {diff} кКал"
        else:
            info = "Хватит есть!"
        return info

    def get_week_stats(self):
        calories_spend_last_week = super().get_week_stats()
        return f"За последнюю неделю было получено {calories_spend_last_week} кКал."


