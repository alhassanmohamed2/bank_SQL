import sqlite3
from datetime import datetime

conn = sqlite3.connect('bank.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

def get_positive_integer_input( prompt):
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                print("\nValue must be a positive number.")
            else:
                return value
        except ValueError:
            print("\nInvalid input. Please enter a valid number.") 

class Account():
    def __init__(self, account_number: int,  pin: int, fname= None, lname =None, balance: int =None):
      
        cursor.execute(f"SELECT * FROM account WHERE id={account_number}")
        row = cursor.fetchone()
        if(row):
            if(
            pin == row['pin'] and
            fname in (row['first_name'] , None) and
            lname in (row['last_name'], None) and
            balance == None
            ):
                self.account_number = row['id']
                self.fname=row['first_name']
                self.lname=row['last_name']
                self._balance=row['balance']
                self._pin=row['pin']
            else:
                print("Wrong account detailes")
                exit()
        elif not row and any(data != None for data in [fname, lname, balance]):
            self.account_number=account_number
            self.fname=fname
            self.lname=lname
            self._balance=balance
            self._pin=pin
            cursor.execute(f"""
                    Insert into account(id, first_name, last_name, balance, pin) 
                        values('{account_number}', '{fname}', 
                                    '{lname}', {balance}, {pin})
                        """)
            cursor.execute(f"""
                     Insert into bank_transaction(type, amount, account_id, to_account_id, date) 
                        values('initial balance', {self.balance},{self.account_number}, 
                                    {self.account_number}, '{datetime.now()}');
                        """)

            conn.commit()
        else:
            print("Error handling data")
            exit()
    @property
    def balance(self):
        return self._balance
    
    @balance.setter
    def balance(self, new_balance):
        self._balance = new_balance
    #################################################
    def deposit(self):
        amount=get_positive_integer_input("Enter the amount: ")
        self.balance +=amount
        self.update_balance('deposit', self.account_number ,self.account_number, amount)
        return self.check_balance()
    #############################################
    def withdraw(self):
        amount=get_positive_integer_input("Enter the amount: ")
        if amount > self.balance:
            return "\nInsufficient balance." + self.check_balance()
        else: 
            self.balance -=amount
            conn.commit()
            self.update_balance('withdraw',self.account_number,'null', amount)
            return self.check_balance()  
    #####################################
    def transfer(self,receiver_account):
        amount=get_positive_integer_input("Enter the amount: ")
        
        if amount > self.balance:
            return "\nInsufficient balance. "+ self.check_balance()
        elif self.account_number == receiver_account:
            return "\nCannot transfer to the same account."
        else:
            self.balance -=amount
            self.update_balance('transfer', self.account_number, receiver_account, -amount)
            self.update_balance('deposit', receiver_account,  self.account_number, amount)
            return self.check_balance()
    ##################################################        
    def update_balance(self, type,from_account_id ,to_account_id, amount):
            cursor.execute(f"""
                    UPDATE account
                    SET balance =  balance + {amount}
                    WHERE id = {from_account_id};
                        """)
            cursor.execute(f"""
                     Insert into bank_transaction(type, amount, account_id, to_account_id, date) 
                        values('{type}', {amount},{from_account_id}, 
                                    {to_account_id}, '{datetime.now()}');
                        """)
            conn.commit()
    def check_balance(self):
        return f"\nYour current balance is: {self.balance} Treat."
    
    




account=""
response = get_positive_integer_input("please enter 1 if you have an account or 2 if you want to create one: \n")
if(response == 1):
    account_number = get_positive_integer_input("Welcome to Meowbank. Please Enter your account number: \n")
    pin=get_positive_integer_input("Enter your pin: ")
    account = Account(account_number, pin)
elif(response == 2):
    first_name = input("Enter Your first name: ")
    last_name = input("Enter Your last name: ")
    pin = get_positive_integer_input("Enter Your pin: ")
    balance = get_positive_integer_input('Enter Your balance: ')
    cursor.execute(f"SELECT max(id) as id FROM account")
    account_number = cursor.fetchone()['id'] + 1
    account = Account(account_number, pin, first_name, last_name, balance)
else:
    print("invalid input")

    

while True:
    
    print("\nChoose one of the following options in the menu:")
    print("(1) Check your balance")
    print("(2) Make a deposit")
    print("(3) Make a withdrawal")
    print("(4) Make a transfer")
    print("(5) Exit the program")
    
    process = input("Enter your choice: ")
    
    if process=="1":
        print(account.check_balance())
    
    elif process=="2":
        print(account.deposit())

    elif process=="3":
        print(account.check_balance())
        print(account.withdraw())
    
    elif process=="4":
        receiver_account_number = get_positive_integer_input("Enter receiver's account number: ")
        cursor.execute(f"SELECT id FROM account where id = {receiver_account_number}")
        receiver_account_number = cursor.fetchone()
        if receiver_account_number:
            receiver_account = receiver_account_number['id']
            print(account.transfer(receiver_account))
        else:
            print("Receiver's account not found.")
    
    elif process=="5":
       exit()
    else:
        print("\nInvalid option.")

