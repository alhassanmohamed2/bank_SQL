import sys

# Define the Account class to represent user accounts
class Account():
    def __init__(self, account_number: int, fname, lname, balance: int, pin: int):
        # Initialize account attributes
        self.account_number=account_number
        self.fname=fname
        self.lname=lname
        self._balance=balance
        self._pin=pin
     
    # Define property to access PIN (read-only)   
    @property
    def pin(self):
        return self._pin
    
    # Define property to access balance (read-only)
    @property
    def balance(self):
        return self._balance
    
    # Define balance setter method to update balance
    @balance.setter
    def balance(self, new_balance):
        self._balance = new_balance

# Function to check and display account balance
def check_balance(account):
    return f"\nYour current balance is: {account.balance} Treat."

# Function to deposit funds into the account
def deposit(account):
    amount=get_positive_integer_input("Enter the amount: ")
    account.balance +=amount
    return f"\nSuccessful deposit. Your new balance is: {account.balance} Treat."

# Function to withdraw funds from the account 
def withdraw(account):
    amount=get_positive_integer_input("Enter the amount: ")
    if amount > account.balance:
        return "\nInsufficient balance." + check_balance(account)
    else: 
        account.balance -=amount
        return f"\nSuccessful withdrawal. Your new balance is: {account.balance} Treat."   

# Function to transfer funds from one account to another
def transfer(sender_account,receiver_account):
    amount=get_positive_integer_input("Enter the amount: ")
      
    if amount > sender_account.balance:
        return "\nInsufficient balance. "+ check_balance(sender_account)
    elif sender_account==receiver_account:
        return "\nCannot transfer to the same account."
    else:
        sender_account.balance -=amount
        receiver_account.balance +=amount
        return f"\nSuccessful transfer. Your new balance is: {sender_account.balance} Treat."

# Function to validate and get positive integer input from user
def get_positive_integer_input(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                print("\nValue must be a positive number.")
            else:
                return value
        except ValueError:
            print("\nInvalid input. Please enter a valid number.")

# Main function to handle user interaction and account operations
def main():
    # Sample account data
    accounts= {
        1: Account(1,"Hamasa","Abosha5a",100,123),
        2: Account(2,"Besla", "Hanem",200,456),
        3: Account(3,"Lotion", "Sarena",75,789)
    }
    
    # Prompt user for account number
    account_number = get_positive_integer_input("Welcome to Meowbank. Please Enter your account number: ")
    
    # Check if the entered account number exists
    if account_number in accounts:
        account=accounts[account_number]
        pin=get_positive_integer_input("Enter your pin: ")

        # Check if the entered PIN matches the account's PIN
        if pin==account.pin:
            print(f"\nSuccessful login. \nHello, {account.fname}.")
            
            # Main menu loop for account operations
            while True:
                print("\nChoose one of the following options in the menu:")
                print("(1) Check your balance")
                print("(2) Make a deposit")
                print("(3) Make a withdrawal")
                print("(4) Make a transfer")
                print("(5) Exit the program")
                
                # Prompt user for action choice
                process = input("Enter your choice: ")
                
                # Execute the chosen action based on user input
                if process=="1":
                    print(check_balance(account))
                
                elif process=="2":
                    print(deposit(account))

                elif process=="3":
                    print(check_balance(account))
                    print(withdraw(account))
                
                elif process=="4":
                    receiver_account_number = get_positive_integer_input("Enter receiver's account number: ")
                    if receiver_account_number in accounts:
                        receiver_account = accounts[receiver_account_number]
                        print(transfer(account, receiver_account))
                    else:
                        print("Receiver's account not found.")
                
                elif process=="5":
                    sys.exit("\nThank you for using the program, Meow you later :)")
                else:
                    print("\nInvalid option.")


        else:
            print("\nWrong password.")
    
    else:
        print("\nAccount not found.")


# Entry point of the program
if __name__ == "__main__":
    main()