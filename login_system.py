import sqlite3

# Connect to database
connection = sqlite3.connect("login_test.db")
cursor = connection.cursor()

# Create table and insert demo user if not exists
cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('demo', 'password123')")
connection.commit()

print("===== Demo Login System =====")

username = input("Enter username: ")
password = input("Enter password: ")

# Vulnerable SQL query using f-string
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"

print(f"[DEBUG] Executing Query: {query}") 

cursor.execute(query)
result = cursor.fetchone()

if result:
    print("Login successful!")
else:
    print("Invalid username or password.")

connection.close()
