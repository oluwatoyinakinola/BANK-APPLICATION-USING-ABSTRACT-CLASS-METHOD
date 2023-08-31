import json
import random

class Database:
    def __init__(self):
        self.customers = []
        self.agents = []
        self.load_data()

    def load_data(self):
        try:
            with open('database.json', 'r') as file:
                self.data = json.load(file)
                self.customers = self.data.get('customers', [])
                self.agents = self.data.get('agents', [])
        except FileNotFoundError:
            self.data = {'customers': [], 'agents': []}
            self.customers = []
            self.agents = [] 

    def save_data(self):
        with open('database.json', 'w') as file:
            json.dump(self.data, file)

    def generate_account_number(self):
        return str(random.randint(1000000000, 9999999999))

    def create_customer_account(self, first_name, last_name, email, pin, balance):
            
        customer = {
            'account_number': self.generate_account_number(),
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'pin': pin,
            'balance': balance
        }
        self.data['customers'].append(customer)
        self.save_data()
        return customer
    
    def create_agent_account(self, first_name, last_name, email, pin, balance):
    
        agent = {
            'account_number': self.generate_account_number(),
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'pin': pin,
            'balance': balance
            
        }
        self.data['agents'].append(agent)
        self.save_data()
        return
    
    def get_customer_by_email(self, email):
        for customer in self.customers:
            if customer['email'] == email:
                return customer
        return None
    
    
    def get_customer(self, account_number):
        for customer in self.data['customers']:
            if customer['account_number'] == account_number:
                return customer
        return None
    
    def get_agent_by_email(self, email):
        for agent in self.agents:
            if agent['email'] == email:
                return agent
        return None
    

    def update_balance(self, account_number, new_balance):
        for customer in self.data['customers']:
            if customer['account_number'] == account_number:
                customer['balance'] = new_balance
                self.save_data()
                return True
        return False
    
    def update_agent_balance(self, account_number, new_balance):
        for customer in self.data['agents']:
            if customer['account_number'] == account_number:
                customer['balance'] = new_balance
                self.save_data()
                return True
        return False

    def reset_password(self, account_number, new_password):
        
        for customer in self.data['customers']:
            if customer['account_number'] == account_number:
                customer['pin'] = new_password
                self.save_data()
                return True
        return False
    
    def reset_agent_password(self, account_number, new_password):
        for customer in self.data['agents']:
            if customer['account_number'] == account_number:
                customer['pin'] = new_password
                self.save_data()
                return True
        return False
    
    def deposit(self, customer_account_number, amount):
        customer_info = self.get_customer(customer_account_number)

        if customer_info:
            customer_balance = customer_info['balance']
            if amount > 0:
              customer_balance += float(amount)
              self.update_balance(customer_account_number, customer_balance)  
              print("Deposit successful.")
            else:
              print("Deposit failed: Invalid amount.")
        else:
            print("Customer not found.")

    def delete_customer(self, account_number):
        for customer in self.customers:
            if customer['account_number'] == account_number:
                self.customers.remove(customer)
                self.data['customers'] = self.customers
                self.save_data()
                return True
        return False
    
