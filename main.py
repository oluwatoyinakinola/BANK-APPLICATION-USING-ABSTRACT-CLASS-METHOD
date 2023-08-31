from database import Database
from customer import Customer
from agent import Agent

def main():
    database = Database()

    while True:
        print("\nWelcome to the Bank System!")
        print("1. Create Account as a Customer")
        print("2. Create an Agent Account")
        print("3. Login as Customer")
        print("4. Login as Agent")
        print("5. Exit")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            create_customer_account(database)
        elif choice == 2:
            create_agent_account(database)
        elif choice == 3:
            customer_actions(database)
        elif choice == 4:
            agent_actions(database)
        elif choice == 5:
            break
        else:
            print("Invalid choice. Please try again.")

def create_customer_account(database):
    customer = Customer.create_account()
    database.create_customer_account(
        customer.first_name, customer.last_name, customer.email, customer._BankAccount__pin, customer.balance
    )
    print("Customer account created successfully!")

def create_agent_account(database):
    agent = Agent.create_account()
    database.create_agent_account(
      agent.first_name, agent.last_name, agent.email, agent._BankAccount__pin, agent.balance
    )
    print("Agent account created successfully.")



          
def customer_actions(database):
    email = input("Enter your email: ")
    pin = input("Enter your PIN: ")
    customer = database.get_customer_by_email(email)

    if customer and customer['pin'] == pin:
        customer_obj = Customer(
            customer['first_name'], customer['last_name'], customer['email'], customer['pin'], customer['balance']
        )
        while True:
            print("\nCustomer Actions: For " + customer['email'])
            print("1. View account information")
            print("2. Make a transfer")
            print("3. Reset password")
            print("4. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                customer_obj.view_account_info()
            elif choice == "2":
                recipient_account = input("Enter recipient's account number: ")
                amount = float(input("Enter the amount to transfer: "))
                transfer_pin = input("Enter your PIN: ")
                recipient = database.get_customer(recipient_account)
                sender_account_number = customer['account_number']
                if recipient:
                    recipient_obj = Customer(
                        recipient['first_name'], recipient['last_name'], recipient['email'], recipient['pin'], recipient['balance']
                    )
                    customer_obj.make_transfer(sender_account_number,recipient_account, amount, transfer_pin)
                else:
                    print("Recipient account not found.")
            elif choice == "3":
                sender_account_number = customer['account_number']
                old_password = input("Enter old password (or leave empty if not applicable): ")
                new_password = input("Enter new password: ")
                customer_obj.reset_password(sender_account_number,new_password, old_password)
            elif choice == "4":
                break
            else:
                print("Invalid choice. Please try again.")
    else:
        print("Invalid login credentials.")



def agent_actions(database):
    email = input("Enter your email: ")
    pin = input("Enter your PIN: ")
    agent = database.get_agent_by_email(email)

    if agent and agent['pin'] == pin:
        agent_obj = Agent(
            agent['first_name'], agent['last_name'], agent['email'], agent['pin'], agent['balance']
        )
        while True:
            print("\nAgent Actions:")
            print("1. Fund customer account")
            print("2. Reset customer's PIN")
            print("3. Delete customer account")
            print("4. Reset account PIN")
            print("5. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                customer_account_number = input("Enter customer's account number: ")
                amount = float(input("Enter the amount to fund: "))
                agentaccount = agent['account_number']
                agentbalance = agent['balance']
                agent_obj.fund_customer_account(agentaccount,customer_account_number, amount, agentbalance)
            elif choice == "2":
                
                customer_account_number = input("Enter customer's account number: ")
                new_pin = input("Enter new PIN: ")
                agent_obj.reset_customer_pin(customer_account_number, new_pin)
            elif choice == "3":
                customer_account_number = input("Enter customer's account number: ")
                confirmation = input("Are you sure you want to delete this customer's account? (yes/no): ")
                agent_obj.delete_customer_account(customer_account_number, confirmation)
            elif choice == "4":
                agent_acct_number = agent['account_number']
                old_password = input("Enter your old password (or leave empty if not applicable): ")
                new_pin = input("Enter new PIN: ")
                agent_obj.reset_account_pin(agent_acct_number, new_pin, old_password)
            elif choice == "5":
                break
            else:
                print("Invalid choice. Please try again.")
    else:
        print("Invalid login credentials.")


if __name__ == "__main__":
    main()
