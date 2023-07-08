import psycopg2
from pwGen import hasher, generator, checker

#creates and insert a new user to the users table
def create_user(username, password):
    salt = generator(32)
    to_be_hashed = salt + password
    hashed_password = hasher(to_be_hashed)

    conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="password", port=8008)
    cur = conn.cursor()
    query = """INSERT INTO users (username, password, salt) VALUES (%s, %s, %s)"""
    parameters = (username, hashed_password, salt)
    cur.execute(query, parameters)
    conn.commit()
    cur.close()
    conn.close()

#check to see if the login credentials is valid
def login_attempt(username, password):
    conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="password", port=8008)
    cur = conn.cursor()
    query = """SELECT salt, password FROM users WHERE username = %(name)s"""
    cur.execute(query, { 'name': username })
    result = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if result:
        salt = result[0]
        salted_password = salt + password
        hashed_password = result[1]
        return checker(salted_password, hashed_password)
    else:
        return False

#gets data of the user
def get_data(username):
    conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="password", port=8008)
    cur = conn.cursor()
    query = """SELECT id, password, salt FROM users WHERE username = %(name)s"""
    cur.execute(query, { 'name': username })
    result = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return result

#creates an account tied to the current user
def create_account(userid, username, email, password, website):
    conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="password", port=8008)
    cur = conn.cursor()
    query = """INSERT INTO accounts (userID, username, email, password, website) VALUES (%s, %s, %s, %s, %s)"""
    parameters = (userid, username, email, password, website)
    cur.execute(query, parameters)
    conn.commit()
    cur.close()
    conn.close()

#gets password based on website
def get_website_pw(userid, website):
    conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="password", port=8008)
    cur = conn.cursor()
    query = """SELECT username, email, password FROM accounts WHERE userid = %(userid)s AND website = %(website)s"""
    cur.execute(query, { 'userid': userid, 'website': website })
    result = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return result

#gets all associated accounts of the current user
def get_all_accounts(userid):
    conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="password", port=8008)
    cur = conn.cursor()
    query = """SELECT username, email, website FROM accounts WHERE userid = %(userid)s"""
    cur.execute(query, { 'userid': userid })
    result = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return result
