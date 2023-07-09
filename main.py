from db_manager import create_user, login_attempt, get_data, create_account, get_website_pw, get_all_accounts, delete_account, update_account
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

def get_accounts(userid, key):
    data = get_all_accounts(userid)
    ids = []
    if not data:
        print('No accounts associated with the provided data')
    else:
        count = 1
        for row in data:
            print('Account ' + str(count))
            print('Username: ' + row[0] + '\nEmail: ' + row[1] + "\nWebsite/Service: " + row[2] + '\n')
            ids.append(row[3])
            count += 1
    return ids, data

def inputs():
    username = input('Enter a new username: ')
    email = input('Enter the email associated to this account: ')
    password = input('Enter the password associated to this account. Alternatively type \"c\" to generate a secure password for this account: ')
    if password == 'c' or password == 'C':
        password = passwordGen()
        pyperclip.copy(password)
        print('Your newly generated password has been copied to your clipboard!')
    website = input('Enter the website/service associated to this account: ')
    return username, email, password, website

def accountInput(string, size):
    invalidInput = True
    while invalidInput:
        try:
            invalidInput = False
            accountVal = int(input(string))
            if accountVal < 0 or accountVal > size:
                raise ValueError
        except:
            invalidInput = True
            print("ERROR: Invalid input\nPlease select a valid account number")
    return accountVal

def updateMenu(username, email, password, website, encrypted_password, key):
    decision = input('Reveal password of chosen account? (Y/N): ')
    
    choice = ''
    border = '-' * 50 + '\n'
    while choice != 'Q':
        string = 'Select an option\n1: Edit Username (%s)\n2: Edit Email (%s)\n3: Edit Website/Service (%s)\n4: Edit Password ' % (username, email, website)
        if decision == 'y' or decision == 'Y':
            string = string + '(' + password + ')'
        string = string + '\nEnter Q to quit Editing\n'

        choice = input(border + string + border)

        if choice == '1':
            username = input('Edit username: ')
        if choice == '2':
            email = input('Edit email: ')
        if choice == '3':
            website = input('Edit website/service: ')
        if choice == '4':
            password = input('Enter the password associated to this account. Alternatively type \"c\" to generate a secure password for this account: ')
            if password == 'c' or password == 'C':
                password = passwordGen()
            encrypted_password = encrypt(key, password)
    return username, email, encrypted_password, website
            


# User is logged into their account
def logged_in(username):
    data = get_data(username)
    userid = data[0]
    hashed_pw = data[1]
    salt = data[2]
    key = generate_key(hashed_pw, salt)
    border = '-' * 50 + '\n'
    string = 'HELLO %s\n1: Print all accounts tied to this account\n2: Create a new account\n3: Find Password for Website\n4: Update a account\n5: Delete a account\n6: Password Generator\nQ: Quit\n' % username
    y = 'y'
    while y != 'Q':
        y = input(border*2 + string + border*2)
        if y == '1':
            get_accounts(userid, key)
            input('Press Any Key to Continue... ')
        if y == '2':
            username, email, password, website = inputs()
            encrypted_password = encrypt(key, password)
            create_account(userid, username, email, encrypted_password, website)
            print('Account Created')
            input('Press Any Key to Continue... ')
        if y == '3':
            website = input('Enter the website/service you need the password to: ')
            data = get_website_pw(userid, website)
            if not data:
                print('No accounts associated with the provided data')
                input('Press Any Key to Continue... ')
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
                print('End of Accounts with associated website \"' + website '\"')
                input('Press Any Key to Continue... ')
        if y == '4':
            ids, data = get_accounts(userid, key)
            if not ids: 
                continue
            accountVal = accountInput('Select the account number you wish to update, or 0 to Quit: ', len(ids))
            if accountVal == 0:
                continue
            else:
                index = accountVal-1
                username, email, encrypted_password, website = updateMenu(data[index][0], data[index][1], decrypt(key, data[index][4]), data[index][2], data[index][4], key)
                update_account(ids[index], userid, username, email, encrypted_password, website)
                print('Account Updated')
                input('Press Any Key to Continue... ')
        if y == '5':
            ids, data = get_accounts(userid, key)
            if not ids: 
                continue
            accountVal = accountInput('Select the account number you wish to delete, or 0 to Quit: ', len(ids))
            if accountVal == 0:
                continue
            else:
                delete_account(userid, ids[accountVal-1])
                print('Account Deleted')
                input('Press Any Key to Continue... ')
        if y == '6':
            print(passwordGen() + '\n')
            input('Press Any Key to Continue... ')
        

# Login menu
x = 'x'
while x != 'Q':
    border = '-' * 25 + '\n'
    string = 'LOGIN\n1: Login to an account\n2: Create a new account\nQ: Quit\n'
    x = input(border*2 + string + border*2)
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
exit()
