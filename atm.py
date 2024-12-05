from DataBase.database import Database
from account import Account

class ATM:
    def __init__(self):
        self.accounts = {}

    def add_account(self, account):
        """حساب‌ها را به دستگاه ATM اضافه می‌کند."""
        self.accounts[account.account_number] = account

    def process_transaction(self, account):
        """پردازش تراکنش‌های ATM."""
        db = Database()
        
        while True:
            print("\nSelect transaction type:")
            print("1. Deposit")
            print("2. Withdraw")
            print("3. View Transactions")
            print("4. View Balance")
            print("5. Transfer Funds")
            print("6. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':  # Deposit
                amount = float(input("Enter amount to deposit: "))
                account.balance += amount
                db.update_balance(account.account_number, account.balance)
                db.record_transaction(account.account_number, 'deposit', amount, account.balance)
                print(f"Deposited {amount}. New balance is {account.balance}")

            elif choice == '2':  # Withdraw
                amount = float(input("Enter amount to withdraw: "))
                if amount <= account.balance:
                    account.balance -= amount
                    db.update_balance(account.account_number, account.balance)
                    db.record_transaction(account.account_number, 'withdraw', amount, account.balance)
                    print(f"Withdrew {amount}. New balance is {account.balance}")
                else:
                    print("Insufficient funds!")

            elif choice == '3':  # View Transactions
                transactions = db.get_transactions(account.account_number)
                print("\nTransaction history:")
                for txn in transactions:
                    print(f"ID: {txn[0]}, Type: {txn[2]}, Amount: {txn[3]}, Date: {txn[4]}, Balance After: {txn[5]}")

            elif choice == '4':  # View Balance
                print(f"Your current balance is: {account.balance}")

            elif choice == '5':  # Transfer Funds
                recipient_account_number = input("Enter recipient account number: ")
                recipient_account_data = db.get_account(recipient_account_number)
                
                if recipient_account_data:
                    amount = float(input("Enter amount to transfer: "))
                    if amount <= account.balance:
                        # برداشت از حساب مبدا
                        account.balance -= amount
                        db.update_balance(account.account_number, account.balance)
                        db.record_transaction(account.account_number, 'withdraw', amount, account.balance)
                        
                        # واریز به حساب مقصد
                        recipient_account = Account(
                            recipient_account_data['account_number'], 
                            recipient_account_data['pin'], 
                            recipient_account_data['balance']
                        )
                        recipient_account.balance += amount
                        db.update_balance(recipient_account.account_number, recipient_account.balance)
                        db.record_transaction(recipient_account.account_number, 'deposit', amount, recipient_account.balance)
                        
                        print(f"Transferred {amount} to account {recipient_account_number}.")
                    else:
                        print("Insufficient funds!")
                else:
                    print("Recipient account not found.")

            elif choice == '6':  # Exit
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")
