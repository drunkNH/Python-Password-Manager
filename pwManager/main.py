from db_manager import create_user, login_attempt, get_data, create_account, get_website_pw, get_all_accounts
from crypter import generate_key, encrypt, decrypt
from pwGen import generator
import pyperclip

'''
Password Manager created by jrgu
'''

def passwordGen():
    invalidInput = True
    while invalidInput:
        try:
            nChar = input('Specify the desired length: ')
            n = int(nChar)
            invalidInput = False
        except:
            print('\nFAILURE: User did not input an integer\n')
            invalidInput = True
    return generator(n)

# User is logged into their account
def logged_in(username):
    data = get_data(username)
    userid = data[0]
    hashed_pw = data[1]
    salt = data[2]
    key = generate_key(hashed_pw, salt)
    string = 'HELLO %s\n1: Print all accounts tied to this account\n2: Create a new account\n3: Find Password for Website\n4: Password Generator\nQ: Quit\n' % username
    y = input(string)
    while y != 'Q':
        if y == '1':
            data = get_all_accounts(userid)
            if not data:
                print('No accounts associated with the provided data')
            else:
                count = 1
                for row in data:
                    print('Account ' + str(count))
                    print('Username: ' + row[0] + '\nEmail: ' + row[1] + "\nWebsite/Service: " + row[2] + "\n")
                    count += 1
        if y == '2':
            username = input('Enter a new username: ')
            email = input('Enter the email associated to this account: ')
            password = input('Enter the password associated to this account. Alternatively type \"c\" to generate a secure password for this account: ')
            if password == 'c' or password == 'C':
                password = passwordGen()
            website = input('Enter the website/service associated to this account: ')
            encrypted_password = encrypt(key, password)
            create_account(userid, username, email, encrypted_password, website)
        if y == '3':
            website = input('Enter the website/service you need the password to: ')
            data = get_website_pw(userid, website)
            if not data:
                print('No accounts associated with the provided data')
            else:
                count = 1
                for row in data:
                    print('Account ' + str(count))
                    print('Username: ' + row[0] + '\nEmail: ' + row[1])
                    password = decrypt(key, row[2])
                    choice = input('Copy password of current account to clipboard? (Y/N): ')
                    if choice == 'y' or choice == 'Y':
                        pyperclip.copy(password)
                    choice = input('Would you like to reveal the password of the current account? (Y/N): ')
                    if choice == 'y' or choice == 'Y':
                        print(password + '\n')
                    count += 1  
        if y == '4':
            print(passwordGen() + '\n')
        y = input(string)

# Login menu
x = input('LOGIN\n1: Login to an account\n2: Create a new account\nQ: Quit\n')
while x != 'Q':
    if x == '1':
        username = input('Enter your username: ')
        password = input('Enter your password: ')
        login = login_attempt(username, password)
        if login:
            print('\nLOGGED IN')
            logged_in(username)
        else:
            print('FAILURE: Username or Password is incorrect')
    if x == '2':
        username = input('Enter a new username: ')
        password = input('Enter a new password: ')
        create_user(username)
        print('Account created...')

    x = input('\nLOGIN\n1: Login to an account\n2: Create a new account\nQ: Quit\n')
