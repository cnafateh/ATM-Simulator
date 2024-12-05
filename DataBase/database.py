import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name="DataBase/File/atm.db"):
        self.db_name = db_name
        self.create_tables()

    def create_tables(self):
        """جدول حساب‌ها و تراکنش‌ها را در دیتابیس ایجاد می‌کند."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            # ایجاد جدول حساب‌ها
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS accounts (
                    account_number TEXT PRIMARY KEY,
                    pin TEXT NOT NULL,
                    balance REAL NOT NULL
                )
            ''')
            # ایجاد جدول تراکنش‌ها
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    account_number TEXT,
                    type TEXT,  -- 'deposit' یا 'withdraw'
                    amount REAL,
                    date TEXT,
                    balance_after REAL,
                    FOREIGN KEY(account_number) REFERENCES accounts(account_number)
                )
            ''')
            conn.commit()

    def add_account(self, account_number, pin, balance):
        """حساب جدید را به دیتابیس اضافه می‌کند."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO accounts (account_number, pin, balance)
                VALUES (?, ?, ?)
            ''', (account_number, pin, balance))
            conn.commit()

    def get_account(self, account_number):
        """حساب را از دیتابیس می‌خواند."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT account_number, pin, balance FROM accounts
                WHERE account_number = ?
            ''', (account_number,))
            result = cursor.fetchone()
            if result:
                return {"account_number": result[0], "pin": result[1], "balance": result[2]}
            return None

    def update_balance(self, account_number, new_balance):
        """مانده حساب را به روز می‌کند."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE accounts SET balance = ? WHERE account_number = ?
            ''', (new_balance, account_number))
            conn.commit()

    def record_transaction(self, account_number, transaction_type, amount, balance_after):
        """تراکنش جدید را در دیتابیس ذخیره می‌کند."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO transactions (account_number, type, amount, date, balance_after)
                VALUES (?, ?, ?, ?, ?)
            ''', (account_number, transaction_type, amount, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), balance_after))
            conn.commit()

    def get_transactions(self, account_number):
        """تراکنش‌های یک حساب را می‌خواند."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM transactions WHERE account_number = ?
            ''', (account_number,))
            return cursor.fetchall()
