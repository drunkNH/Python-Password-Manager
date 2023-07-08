from argon2 import PasswordHasher
import pyperclip
import string
import random

symbols = '!\"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~'

#hashes password
def hasher(pw):
    ph = PasswordHasher()
    hash = ph.hash(pw)
    return hash

#password generator
def generator(n):
    password = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=n))
    return password

#verifies hash password
def checker(pw, hpw):
    ph = PasswordHasher()
    try:
        ph.verify(hpw, pw)
        valid = True
    except:
        valid = False
    return valid

# Tester code, but can be used as a standalone password generator/hasher
if __name__ == '__main__':
    print('WELCOME...\n')
    x = input('1: Convert a Password to Hash' + '\n2: Generate a Password and convert it to Hash\n')
    if x == '1':
        pw = input('Enter password to be converted\n')
        pyperclip.copy(hasher(pw))
        print('The hash has been copied to your clipboard, the hash is: ' + pyperclip.paste())
    elif x == '2':
        invalidInput = True
        while invalidInput:
            try:
                nChar = input('Specify the desired length: ')
                n = int(nChar)
                invalidInput = False
            except:
                print('\nFAILURE: User did not input an integer\n')
                invalidInput = True
        pyperclip.copy(generator(n))
        print('The password has been copied to your clipboard, the password is: ' + pyperclip.paste())
        print('The hash is: ' + hasher(pyperclip.paste()))
    elif x == '3': # Tester for Checker
        pw = input('Password to be checked: ')
        hashpw = input('Hash to be checked: ')
        if checker(pw, hashpw):
            print('The password and hash matched')
        else:
            print('The password and hash did not match')
    else:
        print('Goodbye')
    