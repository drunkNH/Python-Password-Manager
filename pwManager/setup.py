import psycopg2

#any instances of psycopg2.connect should have parameters changed accordingly to your db
conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="password", port=8008)
cur = conn.cursor()

#db work
cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    salt TEXT NOT NULL UNIQUE
);
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
    id SERIAL PRIMARY KEY,
    userID INT,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    website TEXT NOT NULL,
    FOREIGN KEY (userID) REFERENCES users(id)
);
""")

conn.commit()
cur.close()
conn.close()