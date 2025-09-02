import mysql.connector

# Function to create a new account
def create_account(db, name, pin):
    cursor = db.cursor()
    sql = "INSERT INTO accounts (name, pin, balance) VALUES (%s, %s, %s)"
    cursor.execute(sql, (name, pin, 0))
    db.commit()
    print(f" Account created for {name}. Account Number: {cursor.lastrowid}")

# Function to deposit money
def deposit(db, acc_no, amount):
    cursor = db.cursor()
    sql = "UPDATE accounts SET balance = balance + %s WHERE account_number = %s"
    cursor.execute(sql, (amount, acc_no))
    db.commit()
    if cursor.rowcount:
        print(f" Deposited ₹{amount} to Account No {acc_no}")
    else:
        print(" Account not found.")

# Function to withdraw money
def withdraw(db, acc_no, pin, amount):
    cursor = db.cursor()
    cursor.execute("SELECT balance FROM accounts WHERE account_number = %s AND pin = %s", (acc_no, pin))
    result = cursor.fetchone()
    if result:
        current_balance = result[0]
        if current_balance >= amount:
            sql = "UPDATE accounts SET balance = balance - %s WHERE account_number = %s"
            cursor.execute(sql, (amount, acc_no))
            db.commit()
            print(f" Withdrew ₹{amount} from Account No {acc_no}")
        else:
            print(" Insufficient funds.")
    else:
        print(" Invalid account number or PIN.")

# Function to check balance
def check_balance(db, acc_no, pin):
    cursor = db.cursor()
    sql = "SELECT name, balance FROM accounts WHERE account_number = %s AND pin = %s"
    cursor.execute(sql, (acc_no, pin))
    result = cursor.fetchone()
    if result:
        name, balance = result
        print(f" Account Holder: {name}")
        print(f" Balance: ₹{balance}")
    else:
        print(" Invalid account number or PIN.")

# Main function to run the banking system
def main():
    # Connect to MySQL database
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="", 
            database="banking_system"
        )
    except mysql.connector.Error as err:
        print("Error connecting to database:", err)
        return

    # Menu-driven console interface
    while True:
        print("\n--- Banking System ---")
        print("1. Create Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Check Balance")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter your name: ")
            pin = int(input("Set a 4-digit PIN: "))
            create_account(db, name, pin)
        elif choice == '2':
            acc_no = int(input("Enter Account Number: "))
            amount = float(input("Enter amount to deposit: "))
            deposit(db, acc_no, amount)
        elif choice == '3':
            acc_no = int(input("Enter Account Number: "))
            pin = int(input("Enter your PIN: "))
            amount = float(input("Enter amount to withdraw: "))
            withdraw(db, acc_no, pin, amount)
        elif choice == '4':
            acc_no = int(input("Enter Account Number: "))
            pin = int(input("Enter your PIN: "))
            check_balance(db, acc_no, pin)
        elif choice == '5':
            print(" Exiting...")
            break
        else:
            print(" Invalid choice. Try again.")

    db.close()

if __name__ == "__main__":
    main()
