

def adding_expenses(category = "", amount = ""):

    print("Enter your expenses: ")
    category = input("Enter the category of your expense: ")
    amount = input("Enter the amount of your expense: ")

    if any(entry["category"].lower() == category.lower() for entry in data):
        print("You have already added this expenses")
    else:
        data.append({
            "category": category.lower(),
            "amount": amount.lower(),
        })






