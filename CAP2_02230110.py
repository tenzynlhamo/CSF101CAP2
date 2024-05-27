import os
import random
import string

ACCOUNT_DETAILS_FILE = "accounts.txt"

class FinancialRecord:
    def __init__(self, record_id, secret_key, record_type, current_balance=0.0):
        self.record_id = record_id
        self.secret_key = secret_key
        self.record_type = record_type
        self.current_balance = current_balance

    def adjust_credit(self, amount):
        self.current_balance += amount
        print(f"Dear customer, your account has been credited with BTN {amount}. Your available balance is BTN {self.current_balance}.")

    def adjust_debit(self, amount):
        if amount > self.current_balance:
            print("Not enough money.")
        else:
            self.current_balance -= amount
            print(f"Dear customer, your account has been debited with BTN {amount}. Your available balance is BTN {self.current_balance}.")

    def __str__(self):
        return f"{self.record_id},{self.secret_key},{self.record_type},{self.current_balance}"

class PersonalFinancialRecord(FinancialRecord):
    def __init__(self, record_id, secret_key, current_balance=0.0):
        super().__init__(record_id, secret_key, "Personal", current_balance)

class BusinessFinancialRecord(FinancialRecord):
    def __init__(self, record_id, secret_key, current_balance=0.0):
        super().__init__(record_id, secret_key, "Business", current_balance)

class BankingInfrastructure:
    def __init__(self):
        self.records_storage = {}
        self.load_records()

    def load_records(self):
        if os.path.exists(ACCOUNT_DETAILS_FILE):
            with open(ACCOUNT_DETAILS_FILE, 'r') as file:
                for line in file:
                    record_id, secret_key, record_type, current_balance = line.strip().split(',')
                    current_balance = float(current_balance)
                    if record_type == "Personal":
                        record = PersonalFinancialRecord(record_id, secret_key, current_balance)
                    else:
                        record = BusinessFinancialRecord(record_id, secret_key, current_balance)
                    self.records_storage[record_id] = record

    def save_records(self):
        with open(ACCOUNT_DETAILS_FILE, 'w') as file:
            for record in self.records_storage.values():
                file.write(str(record) + "\n")

    def establish_new_record(self, record_type):
        record_id = ''.join(random.choices(string.digits, k=10))
        secret_key = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        if record_type == "Personal":
            record = PersonalFinancialRecord(record_id, secret_key)
        else:
            record = BusinessFinancialRecord(record_id, secret_key)
        self.records_storage[record_id] = record
        self.save_records()
        print(f"Your account has been created. Record ID: {record_id}, Secret Key: {secret_key}")

    def verify_access(self, record_id, secret_key):
        record = self.records_storage.get(record_id)
        if record and record.secret_key == secret_key:
            print("Access granted.")
            return record
        else:
            print("Invalid record ID or secret key.")
            return None

    def terminate_record(self, record_id):
        if record_id in self.records_storage:
            del self.records_storage[record_id]
            self.save_records()
            print("Your account has been terminated.")
        else:
            print("Record not found.")

    def facilitate_transaction(self, sender_record, recipient_record_id, transaction_amount):
        recipient_record = self.records_storage.get(recipient_record_id)
        if not recipient_record:
            print("Recipient record not found.")
            return
        if sender_record.current_balance < transaction_amount:
            print("Insufficient balance.")
            return
        sender_record.adjust_debit(transaction_amount)
        recipient_record.adjust_credit(transaction_amount)
        self.save_records()
        print(f"Transferred {transaction_amount} to record {recipient_record_id}.")

def initiate_banking_process():
    banking_infrastructure = BankingInfrastructure()
    while True:
        print("\nBanking Infrastructure Menu:")
        print("1. Establish New Personal Record")
        print("2. Establish New Business Record")
        print("3. Verify Access")
        print("4. Exit")
        menu_selection = input("Please select an option: ")

        if menu_selection == '1':
            banking_infrastructure.establish_new_record("Personal")
        elif menu_selection == '2':
            banking_infrastructure.establish_new_record("Business")
        elif menu_selection == '3':
            record_id = input("Enter record ID: ")
            secret_key = input("Enter secret key: ")
            record = banking_infrastructure.verify_access(record_id, secret_key)
            if record:
                while True:
                    print("\nRecord Management Options:")
                    print("1. Adjust Credit")
                    print("2. Adjust Debit")
                    print("3. Facilitate Transaction")
                    print("4. Terminate Record")
                    print("5. Log Out")
                    management_option = input("Choose an action: ")

                    if management_option == '1':
                        amount = float(input("Enter amount to adjust credit: "))
                        record.adjust_credit(amount)
                        banking_infrastructure.save_records()
                    elif management_option == '2':
                        amount = float(input("Enter amount to adjust debit: "))
                        record.adjust_debit(amount)
                        banking_infrastructure.save_records()
                    elif management_option == '3':
                        recipient_record_id = input("Enter recipient record ID: ")
                        amount = float(input("Enter transaction amount: "))
                        banking_infrastructure.facilitate_transaction(record, recipient_record_id, amount)
                    elif management_option == '4':
                        banking_infrastructure.terminate_record(record.record_id)
                        break
                    elif management_option == '5':
                        print("Logging out.")
                        break
                    else:
                        print("Invalid option. Please try again.")
        elif menu_selection == '4':
            print("Exiting.")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    initiate_banking_process()
