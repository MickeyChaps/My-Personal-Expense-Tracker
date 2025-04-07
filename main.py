#Importing all important libraries and functions(from other files as well

import sqlite3
from menuz import *
from expense_tracker_functions import Functions

def main():
    #we do this because other programs are importing the same things as the main program
    functions = Functions()


    #Connect to the database
    conn = sqlite3.connect("expense_tracker.db")
    cur = conn.cursor()

    cur.executescript('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            email EMAIL NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS Expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            expense_name TEXT NOT NULL,
            amount INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES Users (id)
        );
        
        CREATE TABLE IF NOT EXISTS Userlogin(
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES Users (id)
        );
    ''')

    conn.commit()
    conn.close()


    print("Welcome to the Personal Expense Tracker")
    print("=================================================================================")

    #Using the Login menu
    first_message =  menu1()



main()






