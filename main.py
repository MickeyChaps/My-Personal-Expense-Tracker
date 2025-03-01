#Importing all important libraries and functions(from other files as well)

import json
from menuz import *
#from adding_expenses_function import *

#Our Global variables
name = ""
#expense = ""
age = ""
phone = ""

#Opening and loading our JSON file in the "Read" mode
try:
    with open("expenses.json", "r") as json_file:
        data = json.load(json_file)
        #Helps to load the file properly
        if not isinstance(data, dict):
            data = []
except (FileNotFoundError, json.decoder.JSONDecodeError):
    #If the file is not found, generate a new JSON file with a dictionary "data"
    data = []
    #expenses = []

print("Welcome to the Personal Expense Tracker")
print("=================================================================================")

#Using the Login menu
first_message =  menu1("1")

#Registration of new user
if first_message == "1":
    print("Enter your:")
    name = input("1. Full Name: ")
    age = input("2. Your age: ")
    phone = input("3. Phone Number: ")

    #Checking whether the User exists using the dictionary Key
    if any(entry["name"].lower() == name.lower() for entry in data):
        print("User already exists!!!!")
    else:
        new_entry = {"name": name,
                     "age": age,
                     "phone": phone,
                     }
        data.append(new_entry)
        print("Account Successfully Registered")

        with open("expenses.json", "w") as file:
            json.dump(data, file, indent=4)
        #Using the Operations menu
        second_message = menu2("2")






