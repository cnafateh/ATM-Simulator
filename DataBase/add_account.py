from database import Database

def add_new_account():
    db = Database()  # اتصال به دیتابیس
    account_number = input("Enter account number: ")
    pin = input("Enter PIN: ")
    balance = float(input("Enter initial balance: "))
    
    db.add_account(account_number, pin, balance)
    print("Account added successfully.")

if __name__ == "__main__":
    add_new_account()
