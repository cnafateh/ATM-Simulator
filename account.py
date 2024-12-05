class Account:
    def __init__(self, account_number, pin, balance=0):
        self.account_number = account_number
        self.pin = pin
        self.balance = balance
        self.transactions = []  # برای ذخیره تراکنش‌ها

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.transactions.append(f"Deposited {amount}")
            return True
        return False

    def withdraw(self, amount):
        if amount > 0 and self.balance >= amount:
            self.balance -= amount
            self.transactions.append(f"Withdrew {amount}")
            return True
        return False

    def check_balance(self):
        return self.balance

    def transfer(self, target_account, amount):
        if self.withdraw(amount):
            target_account.deposit(amount)
            self.transactions.append(f"Transferred {amount} to account {target_account.account_number}")
            return True
        return False

    def get_transactions(self):
        return self.transactions

    def authenticate(self, pin):
        return self.pin == pin
