from database import Database
import sqlite3

def delete_account():
    db = Database()  # اتصال به دیتابیس
    account_number = input("Enter the account number to delete: ")
    
    # حذف حساب از دیتابیس
    with sqlite3.connect(db.db_name) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM accounts WHERE account_number = ?
        ''', (account_number,))
        conn.commit()
    
    print(f"Account with account number {account_number} has been deleted.")

def edit_account():
    db = Database()  # اتصال به دیتابیس
    account_number = input("Enter the account number to edit: ")
    
    # خواندن اطلاعات حساب از دیتابیس
    account_data = db.get_account(account_number)
    
    if account_data:
        print(f"Current PIN: {account_data['pin']}")
        print(f"Current Balance: {account_data['balance']}")
        
        new_pin = input("Enter new PIN (or press Enter to keep current): ")
        new_balance = input("Enter new balance (or press Enter to keep current): ")
        
        if new_pin:
            account_data['pin'] = new_pin
        if new_balance:
            account_data['balance'] = float(new_balance)
        
        # به روزرسانی اطلاعات حساب در دیتابیس
        with sqlite3.connect(db.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE accounts
                SET pin = ?, balance = ?
                WHERE account_number = ?
            ''', (account_data['pin'], account_data['balance'], account_number))
            conn.commit()
        
        print("Account information updated successfully.")
    else:
        print("Account not found.")

while True:
    print("Delete. 1\nEdit. 2")
    choise = input("Enter your choice: ")
    if choise == "1":
        delete_account()
        break
    elif choise == "2":
        edit_account()
        break
    else:
        print("Invalid choice. Please try again.")