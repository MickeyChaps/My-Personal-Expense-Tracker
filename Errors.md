📌 ERROR CATALOGUE: DATABASE CONNECTION & USER INPUT ISSUES
1️⃣ sqlite3.OperationalError: database is locked
🔍 What Causes It?
This happens when two database connections are trying to write at the same time.
It also occurs if a previous database connection wasn't properly closed, leaving the database locked.
If the program crashes or doesn’t commit() changes before closing the connection, SQLite can keep the DB locked.
🛠️ How to Fix It?
✅ Make sure you close every database connection properly

python
Copy
Edit
conn.commit()
conn.close()
✅ Use a single connection per function

Instead of keeping the connection open across multiple functions, open and close it in the same function where it's used.
If you need a persistent connection, use with sqlite3.connect("database.db") as conn: to ensure proper closing.
✅ Kill any stuck database processes

If the DB is still locked, close the script and delete any *.db-wal or *.db-shm files before restarting.
2️⃣ sqlite3.IntegrityError: NOT NULL constraint failed
🔍 What Causes It?
This happens when you try to insert NULL (empty) values into a column that does not allow NULL values.
In our case, this happened because the user_id wasn't getting retrieved properly after registration, so it was inserting NULL instead.
🛠️ How to Fix It?
✅ Ensure the user_id is retrieved before using it
We fixed this by returning the user_id from register_user() immediately after inserting the user instead of fetching it later.

python
Copy
Edit
def register_user(self, name, email, age):
    conn = sqlite3.connect("expense_tracker.db")
    cur = conn.cursor()

    cur.execute("INSERT INTO Users (name, email, age) VALUES (?, ?, ?)", (name, email, age))
    conn.commit()

    user_id = cur.lastrowid  # ✅ Get the ID of the newly inserted user
    conn.close()
    
    return user_id  # ✅ Return user_id for further use
✅ Always check if user_id is None before inserting into another table

python
Copy
Edit
if user_id is not None:
    functions.setlogincredentials(username, password, user_id)
else:
    print("Error: Could not retrieve user ID")
3️⃣ sqlite3.OperationalError: no such column: user_id
🔍 What Causes It?
This happens when the column you're referencing doesn't exist in the table.
In our case, this happened because the table was not created correctly or we were using the wrong table/column name in a query.
🛠️ How to Fix It?
✅ Double-check the table schema
Make sure that the column actually exists in the table before using it in a query:

python
Copy
Edit
CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email EMAIL NOT NULL,
    age INTEGER NOT NULL
);
✅ Ensure correct table and column names in queries

If you get this error, print the available columns:
python
Copy
Edit
cur.execute("PRAGMA table_info(Expenses)")
print(cur.fetchall())  # Shows all columns in the table
Fix any typos in your column names. Example:
python
Copy
Edit
cur.execute("SELECT user_id FROM Expenses WHERE expense_name = ?", (expense_name,))
Make sure user_id actually exists in Expenses.

4️⃣ TypeError: setlogincredentials() missing 1 required positional argument: 'user_id'
🔍 What Causes It?
This happens when a function is expecting an argument that wasn’t provided.
We got this error because setlogincredentials() was expecting user_id, but user_id was None or missing.
🛠️ How to Fix It?
✅ Make sure user_id is correctly retrieved before calling the function

python
Copy
Edit
user_id = functions.register_user(name, email, age)  # ✅ Get user_id
functions.setlogincredentials(username, password, user_id)  # ✅ Pass user_id properly
✅ Provide all required arguments when calling a function

python
Copy
Edit
def setlogincredentials(self, username, password, user_id):  # ✅ Expect user_id
5️⃣ sqlite3.IntegrityError: UNIQUE constraint failed
🔍 What Causes It?
This error occurs when trying to insert a duplicate value into a column that has a UNIQUE constraint.
Example: If the email column in Users is UNIQUE, trying to register the same email twice causes this error.
🛠️ How to Fix It?
✅ Check if a record exists before inserting

python
Copy
Edit
cur.execute("SELECT * FROM Users WHERE email = ?", (email,))
existing_user = cur.fetchone()

if existing_user:
    print("User already exists")  # ✅ Prevent duplicate entry
else:
    cur.execute("INSERT INTO Users (name, email, age) VALUES (?, ?, ?)", (name, email, age))
    conn.commit()
✅ Use INSERT OR IGNORE to prevent duplicates

python
Copy
Edit
cur.execute("INSERT OR IGNORE INTO Users (name, email, age) VALUES (?, ?, ?)", (name, email, age))
conn.commit()
6️⃣ sqlite3.ProgrammingError: Incorrect number of bindings supplied
🔍 What Causes It?
This happens when the number of placeholders (?) in the SQL query does not match the number of values provided.
Example:
python
Copy
Edit
cur.execute("INSERT INTO Users (name, email) VALUES (?, ?, ?)", (name, email))  # ❌ Wrong: 3 placeholders but 2 values
🛠️ How to Fix It?
✅ Make sure the number of values matches the placeholders

python
Copy
Edit
cur.execute("INSERT INTO Users (name, email, age) VALUES (?, ?, ?)", (name, email, age))  # ✅ Correct
✅ Use named placeholders for clarity

python
Copy
Edit
cur.execute("INSERT INTO Users (name, email, age) VALUES (:name, :email, :age)", 
            {"name": name, "email": email, "age": age})
🚀 Summary: How to Avoid These Errors in the Future
✅ 1. Always close the database connection after executing queries
✅ 2. Always check if a record exists before inserting to avoid duplicate errors
✅ 3. Always retrieve and verify foreign keys (user_id) before inserting into another table
✅ 4. Double-check column names when writing queries to avoid "no such column" errors
✅ 5. Ensure the number of ? placeholders matches the number of values passed
✅ 6. If a column has a NOT NULL constraint, always provide a valid value before inserting