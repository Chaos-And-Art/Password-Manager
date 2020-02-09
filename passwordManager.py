import sqlite3
import os
import time
import random
import string
from hashlib import sha256

MASTER_PASSWORD = "12345"

connect = input("Enter Master Password.\n")

while connect != MASTER_PASSWORD:
    connect = input(
        "Incorrect Password. Try again, or type 'Exit' to exit the program.\n")
    if connect == "Exit" or connect == "exit":
        break

database = sqlite3.connect('password_manager.db')
cursor = database.cursor()


def create_password(stringLength=25):
    password_characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(password_characters) for i in range(stringLength))

# def create_hex(service):
#     return sha256(service.lower().encode('utf-8')).hexdigest()

# def get_hex(service):
#     return sha256(service.lower().decode('utf-8')).hexdigest()


def get_password(service):
    getData = ("SELECT password FROM passMan WHERE serviceName = ?")
    cursor.execute(getData, [(service)])

    rows = cursor.fetchall()
    pass_string = ""
    for row in rows:
        pass_string = row[0]

    if pass_string == "":
        return "There is no Password saved for this Service."
    else:
        return pass_string


def store_create_password(name, password):
    insertData = '''INSERT INTO passMan (serviceName, password) VALUES (?,?)'''
    cursor.execute(insertData, [(name), (password)])
    database.commit()


def store_rand_password(name):
    random_password = create_password()
    insertData = '''INSERT INTO passMan (serviceName, password) VALUES (?,?)'''
    cursor.execute(insertData, [(name), (random_password)])
    database.commit()
    return random_password


def random_or_create():
    print("\n" + "Would you like to create your own Password?")
    print(" "*20 + "OR")
    print("Would you like a randomly generated Password?")
    time.sleep(3)
    pass_command_list()
    _type = input("-> ")

    if _type == "Create" or _type == "create":
        serviceName = input(
            "Enter the name you would like the password to be associated with. (Case Sensitive)\n" + "-> ")
        create = input(
            "\n" + "Now enter a password to be associated with " + serviceName + "\n -> ")
        store_create_password(serviceName, create)
        print("\n" + "The Password for " +
              serviceName + " is:\n" + create)

    elif _type == "Random" or _type == "random":
        serviceName = input(
            "Enter the name you would like the password to be associated with. (Case Sensitive)\n" + "-> ")
        print("\n" + "The Password for " + serviceName + " is:\n" +
              store_rand_password(serviceName))
        time.sleep(10)


def menu_command_list():
    print("\n" + "~"*25)
    print("COMMANDS:")
    print("Store = Store Password")
    print("Get = Get Password")
    print("Exit = Exit Program")
    print("~"*25)


def pass_command_list():
    print("\n" + "~"*25)
    print("COMMANDS:")
    print("Create = Create Password")
    print("Random = Random Password")
    print("~"*25)


if connect == MASTER_PASSWORD:
    try:
        cursor.execute('''CREATE TABLE passMan
            (serviceName TEXT NOT NULL, password TEXT NOT NULL);''')
        print("\n" + "You have created a safe!")
        print("What would you like to store in it today?")
        time.sleep(1)
    except:
        print("\n" + "Entered your safe!")
        print("How would you like to proceed?")
        time.sleep(1)

    while True:
        menu_command_list()
        _input = input("-> ")

        if _input == "Exit" or _input == "exit":
            break
        if _input == "Store" or _input == "store":
            random_or_create()

        if _input == "Get" or _input == "get":
            service = input(
                "What is the name of the service? (Case Sensitive)\n" + "-> ")
            print("\n" + service + " password:\n" +
                get_password(service))
            time.sleep(10)
