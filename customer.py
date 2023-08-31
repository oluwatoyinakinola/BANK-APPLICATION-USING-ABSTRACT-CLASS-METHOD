from bank_account import BankAccount
from database import Database

db = Database()

class Customer(BankAccount):
    def __init__(self, first_name, last_name, email, pin, balance=0):
        super().__init__(first_name, last_name, email, pin)
        self.__account_number = self.generate_account_number()
        self.balance = balance

    @classmethod
    def create_account(cls):
        first_name = input("Enter your first name: ")
        last_name = input("Enter your last name: ")
        email = input("Enter your email: ")
        pin = input("Enter a pin: ")
        balance = float(input("Enter initial balance: "))
        return cls(first_name, last_name, email, pin, balance)

    def view_account_info(self):
        print(super().__str__())
        print(f"Account Number: {self.__account_number}")
        
    def reset_account_pin(self, new_pin):
        self._BankAccount__pin = new_pin
        print("Account PIN reset successful.")    

    def reset_password(self, account_number,new_password, old_password=None):
        if old_password is not None and self.authenticate(old_password):
            self._BankAccount__pin = new_password
            db.reset_password(account_number,new_password )
            print("Password reset successful.")
        else:
            print("Invalid old password.")

    def make_transfer(self, sender_account_number,recipient_account_number, amount, pin):
        recipient = db.get_customer(recipient_account_number)
         
        recp_email = recipient['email']
        recipient_agent = db.get_agent_by_email(recp_email)
        print(f"DEBUG: Sender balance before transfer: {self.balance}")
        print(f"DEBUG: Recipient before transfer: {recipient}")
        print(f"DEBUG: Recipient agent before transfer: {recipient_agent}")
        
        if  self.balance >= float(amount) and self.authenticate(pin):
           self.balance = self.balance - float(amount)
           db.update_balance(recipient_account_number, recipient['balance'] + amount)
           db.update_balance(sender_account_number, self.balance)  
           
           db.save_data()   
           print(f"DEBUG: Sender balance after transfer: {self.balance}")
           print("Transfer successful.")
        else:
           print("Transfer failed: Insufficient funds, incorrect PIN, or recipient account not found.")
    
    def deposit(self, amount):
        if amount > 0:
           self.balance += amount
           db.update_balance(self.__account_number, self.balance) 
           print("Deposit successful.")
        else:
            print("Deposit failed: Invalid amount.")

    def to_json(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "pin": self._BankAccount__pin,
            "balance": self.balance,
            "account_number": self.__account_number
        }

    def save_to_file(self):
        database = Database()
        database.create_customer_account(
            self.first_name, self.last_name, self.email, self._BankAccount__pin, self.balance
        )
db = Database()