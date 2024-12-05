from atm import ATM
from account import Account
from DataBase.database import Database

def main():
    db = Database()  # اتصال به دیتابیس

    # ورود به سیستم
    print("Welcome to the ATM")
    account_number = input("Enter your account number: ")
    pin = input("Enter your PIN: ")

    # خواندن حساب از دیتابیس
    account_data = db.get_account(account_number)

    if account_data and account_data["pin"] == pin:
        # ساخت حساب از داده‌های خوانده شده از دیتابیس
        account = Account(account_data["account_number"], account_data["pin"], account_data["balance"])
        print("\nLogin successful!")
        
        # ایجاد دستگاه ATM
        atm = ATM()

        # افزودن حساب‌ها به دستگاه ATM
        atm.add_account(account)

        # پردازش تراکنش‌ها
        atm.process_transaction(account)
    else:
        print("Invalid account number or PIN. Exiting...")

if __name__ == "__main__":
    main()
