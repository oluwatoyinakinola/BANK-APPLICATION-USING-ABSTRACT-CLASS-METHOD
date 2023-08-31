from bank_account import BankAccount
from database import Database

db = Database()

class Agent(BankAccount):
    def __init__(self, first_name, last_name, email, pin, balance=0):
        super().__init__(first_name, last_name, email, pin)
        self.balance = balance

    @classmethod
    def create_account(cls):
        first_name = input("Enter your first name: ")
        last_name = input("Enter your last name: ")
        email = input("Enter your email: ")
        pin = input("Enter a pin: ")
        balance = float(input("Enter initial balance: "))
        return cls(first_name, last_name, email, pin, balance)

    
    @classmethod
    def login(cls, email, pin):
        agents_data = Database.load_data().get('agents', {})
        if email in agents_data.keys() and agents_data[email]['pin'] == pin:
            agent_data = agents_data[email]
            return cls(agent_data['first_name'], agent_data['last_name'], email, pin)
        return None


    def view_account_info(self):
        print(super().__str__())

    def reset_password(self, new_password):
        self._BankAccount__pin = new_password
        print("Agent password reset successful.")
            
    def reset_account_pin(self, agent_account_number,new_pin, old_password=None):
        if old_password is None or self.authenticate(old_password):
            db.reset_agent_password(agent_account_number, new_pin)
            print("Agent's PIN reset successful.")
        else:
            print("Invalid old password.") 
                   
    def fund_customer_account(self, agent_account,customer_account, amount, agent_balance):
        if self.authenticate(self._BankAccount__pin):
            customer_info = db.get_customer(customer_account)
            agent_balance = agent_balance - amount
            if customer_info:
                customer_balance = customer_info['balance'] + amount
                db.update_balance(customer_account, customer_balance)
                db.update_agent_balance(agent_account, agent_balance)
                print("Funding customer account successful.")
            else:
                print("Customer not found.")
        else:
            print("Funding customer account failed: Incorrect agent PIN.")
            
            
    def reset_customer_pin(self, customer_account_number, new_pin):
        db.reset_password(customer_account_number,new_pin )
        print("Customer's PIN reset successful.")
            
            
    def delete_customer_account(self, account_number, confirmation):
        customer = db.get_customer(account_number)
        if customer:
            if confirmation.lower() == 'yes':
                db.delete_customer(account_number)
                print("Customer account deleted.")
            else:
              print("Deletion canceled.")
        else:
            print("Customer not found.")

            

    def to_json(self):
        return {
        "first_name": self.first_name,
        "last_name": self.last_name,
        "email": self.email,
        "pin": self._BankAccount__pin,
        "balance": self.balance
    }
        

    def save_to_file(self):
        database = Database()
        database.create_agent_account(
            self.first_name, self.last_name, self.email, self._BankAccount__pin
        )