# A Python Password Manager using PostgreSQL
![image](https://i.gyazo.com/511deca6ddd9c3a9ba2fe283fc0e7dec.png)

## Purpose
A terminal-based CRUD Password Manager program design to keep a person's passwords to be stored and retrieved using a database, using psycopg2 as the python adapter for PostgreSQL.

Multiple users can use the program, but the program does not allow users to peek at another user's passwords.

A master password is used to "unlock" a user's stored passwords in the database. The master password is salted and hashed using argon2 to secure the master password.

A user's stored passwords is encrypted using the Cryptography library, and only decrypted to the original user.

A password generator is also included, allowing for randomized secured password of variable length chosen by the user.

A user can retrieve an account's passwords by entering the webiste/service associated with the account. In the case of alternative accounts i.e. multiple accounts with the same service, the program will scroll through the accounts with the same requested service

## Libraries used
* psycopg2
* argon2
* base64
* cryptography
* pyperclip
* string
* random

## Setup
1. Install [Postgresql](https://www.postgresql.org/), and setup a Postgresql server using PgAdmin 4 (or whatever your chosen tool for postgresql is)
    * You will need to setup the server which adheres to the parameters ```host="localhost", dbname="postgres", user="postgres", password="password", port=8008)```. 
    * If not, you will need to change the code of each ```psycopg2.connect``` to your parameters accordingly
2. Install the python libraries 
    * These libraries, besides built-in python libraries, were installed using pip
3. Run the setup.py file to create the tables. ```python -m setup```
4. Run main to run the program ```python -m main```
## Side note
You can run pwGen.py ```python -m pwGen``` as a side program to access the password generator and hasher.
