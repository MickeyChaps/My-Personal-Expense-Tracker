import sqlite3



#Class names should have Capita letters
class Functions:
    def __init__(self):
        pass


    def register_user(self, name, email, age):
        conn = sqlite3.connect("expense_tracker.db")
        cur = conn.cursor()

        # Check if user already exists before inserting
        cur.execute("SELECT * FROM Users WHERE email = ?", (email,))
        existing_user = cur.fetchone()

        if existing_user:
            print("User already exists")
            user_id = existing_user[0]

        else:
            cur.execute('''
                INSERT INTO Users (name, age, email) VALUES (?, ?, ?)''', (name, email, age)
                )
            conn.commit()
            user_id = cur.lastrowid
            print("Account Registered successfully")
        conn.close()
        return user_id

    def setlogincredentials(self, username, password, user_id):
        conn = sqlite3.connect("expense_tracker.db")
        cur = conn.cursor()

        cur.execute("INSERT INTO Userlogin(username, password, user_id) VALUES (?, ?, ?)", (username, password, user_id))
        conn.commit()
        conn.close()

        print("Login credentials created successfully")




    def get_user_id(self, email):
        conn = sqlite3.connect("expense_tracker.db")
        cur = conn.cursor()

        cur.execute("SELECT id FROM Users WHERE email = ?", (email,))
        user = cur.fetchone()

        conn.close()
        if user:
            print(f"✅ User ID found: {user[0]}")
            return user[0]
        else:
            print(f"❌ No user found with email: {email}")
            return None


    def edit_expense(self, username, expense_name, amount):
        conn = sqlite3.connect("expense_tracker.db")
        cur = conn.cursor()

        #Fetch the user ID first
        cur.execute("SELECT user_id FROM Userlogin WHERE username = ?", (username,))
        user = cur.fetchone()

        if user:
            user_id = user[0]

            #Check if the user already has an expense with the same name and amount
            cur.execute("SELECT id FROM Expenses WHERE expense_name = ? AND amount = ? AND user_id = ?", (expense_name, amount, user_id))
            exact_expense = cur.fetchone()

            if exact_expense:
                print("Expense already exists")

            else:
                #Check if user has the same expense name but different amount
                cur.execute("SELECT id FROM Expenses WHERE expense_name = ? AND user_id = ?", (expense_name, user_id))
                existing_expense = cur.fetchone()

                if existing_expense:
                    #Update the amount of the existing expense
                    cur.execute('''
                        UPDATE Expenses
                        SET amount = ?
                        WHERE id =?
                    ''', (amount, existing_expense[0]))
                    conn.commit()
                    print("Expense updated successfully")
                else:
                    #Insert new expense record
                    cur.execute('''
                        INSERT INTO Expenses (expense_name, amount, user_id) VALUES (?, ?, ?) 
                        ''', (expense_name, amount, user_id))
                    conn.commit()
                    print("\nExpense added successfully")
                    from menuz import menu2
                    menu2(username)

        else:
            print("User does not exist")
            new_registration = input("Would you like to register? (yes/no): ")
            if new_registration.lower() == "yes":
                from menuz import menu1
                menu1()

            elif new_registration.lower() == "no":
                from menuz import menu3
                menu3()

        conn.close()

    def login(self, username, password):
        conn = sqlite3.connect("expense_tracker.db")
        cur = conn.cursor()

        cur.execute("SELECT * FROM Userlogin WHERE username = ? AND password = ?", (username, password))
        user = cur.fetchone()
        if user:
            print("Login successful\n")
            from menuz import menu2
            menu2(username)

            return user[2]

        else:
            print("Invalid username or password")
            from menuz import menu1
            menu1()
            conn.close()
            return None


    def view_expenses(self, user_id):
        conn = sqlite3.connect("expense_tracker.db")
        cur = conn.cursor()

        # Fetch expenses for the given user_id
        cur.execute("SELECT expense_name, amount FROM Expenses WHERE user_id = ?", (user_id,))
        expenses = cur.fetchall()

        if expenses:
            print("\nYour Expenses:")
            for expense in expenses:
                print(f"- {expense[0]}: ${expense[1]}")
        else:
            print("No expenses found.")

        conn.close()









