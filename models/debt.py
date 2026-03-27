class Debt:
    def __init__(self, name, balance, interest_rate, min_payment):
        self.name = name
        self.balance = balance
        self.interest_rate = interest_rate
        self.min_payment = min_payment

    def apply_interest(self):
        monthly_rate = self.interest_rate / 12
        self.balance *= (1 + monthly_rate)

    def make_payment(self, amount):
        self.balance -= amount
        if self.balance < 0:
            overpay = -self.balance
            self.balance = 0
            return overpay
        return 0

    def is_paid_off(self):
        return self.balance <= 0
