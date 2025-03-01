def menu1(login):
    print("Choose your appropriate option:")
    login = input("1. Sign-up\n2. Login\n3. Exit \n\n")

    if login == "3":
        print("Exiting the program.......")
        exit()
    return login

def menu2(operations):
    print("Choose your appropriate option:")
    operations = input("1. Edit expenses\n2.Expenses Look-Up\n3. Exit\n\n")

    if operations == "3":
        print("Exiting the program.......")
        exit()
    return operations