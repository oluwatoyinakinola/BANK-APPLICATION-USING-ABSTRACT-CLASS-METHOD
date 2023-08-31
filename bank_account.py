from abc import ABC, abstractmethod
import random

class BankAccount(ABC):
    def __init__(self, first_name, last_name, email, pin):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.__pin = pin  
        self.balance = 0.0

    def authenticate(self, entered_pin):
        return self.__pin == entered_pin

    @abstractmethod
    def view_account_info(self):
        pass

    @abstractmethod
    def reset_password(self, new_password):
        pass

    @abstractmethod
    def reset_account_pin(self, new_pin):
        pass
    
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print("Deposit successful.")
        else:
            print("Invalid deposit amount.")

    def generate_account_number(self):
        return str(random.randint(1000000000, 9999999999))

    def __str__(self):
        return f"Name: {self.first_name} {self.last_name}\nBalance: {self.balance}"
