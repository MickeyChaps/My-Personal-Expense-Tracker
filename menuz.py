import sqlite3
from expense_tracker_functions import Functions
import pwinput


functions = Functions()
def menu1():

    print("Choose your appropriate option:")
    login = input("1. Sign-up\n2. Login\n3. Exit \n\n")

    if login == "1":
        print("Enter your:")
        name = input("1. Full Name: ")
        age = input("2. Your age: ")
        email = input("3. Email: ")


        # Fetch the user ID after registration
        user_id = functions.register_user(name, age, email)

        if user_id is None:
            print("Error: User ID not found after registration")
            return

        else:
            print("Set your login credentials: ")
            username = input("4. Username: ")
            password = pwinput.pwinput("5. Password: ")

            functions.setlogincredentials(username, password, user_id)

        second_message = menu2(username)


        if second_message == "1":
            prompt = input("Would you like to add an expense? y/n: ")
            if prompt.lower() == "y":
                expense_name = input("Enter the expense category: ")
                amount = input("Enter your amount spent in USD: ")
                functions.edit_expense(username, expense_name, amount)
            else:
                menu3()
    elif login == "2":
        print("Enter your:")
        username = input("Username: ")
        password = pwinput.pwinput("Password: ")

        success = functions.login(username, password)
        if success:
            menu2(username)
        else:
            menu3()
    else:
        print("Exiting the program.......")
        exit()
    return login

def menu2(username):
    conn = sqlite3.connect("expense_tracker.db")
    cur = conn.cursor()


    cur.execute("SELECT user_id FROM Userlogin WHERE username = ?", (username,))
    user = cur.fetchone()

    if not user:
        print("User not found")
        return

    user_id = user[0]

    while True:
        print("Choose your appropriate option:")
        operations = input("1. Add expenses\n2. View Current Expenses\n3. Delete Expenses\n4. Exit \n\n")

        if operations == "1":
            expense_name = input("Enter the expense category: ")
            amount = input("Enter your amount spent in USD: ")
            functions.edit_expense(username, expense_name, amount)

        elif operations == "2":
            functions.view_expenses(user_id)
            menu2(username)

        elif operations == "3":
            functions.view_expenses(user_id)
            expense_name = input("Which expense would you like to remove?\n")
            cur.execute("DELETE FROM Expenses WHERE expense_name = ?", (expense_name,))
            print("Your expense has been removed successfully")


        elif operations == "4":
            print("Exiting the program.......")
            exit()

        else:
            print("Invalid choice. Try again")

        conn.commit()
        conn.close()
        return operations

def menu3():
    print("Exiting the program.......")
    exit()

