import sqlite3

connection = sqlite3.connect("login_test.db")
cursor = connection.cursor()

print("===== Secure Login System =====")

username = input("Enter username: ")
password = input("Enter password: ")

# SECURE APPROACH: Using '?' placeholders to prevent SQL Injection
query = "SELECT * FROM users WHERE username = ? AND password = ?"

cursor.execute(query, (username, password))
result = cursor.fetchone()

if result:
    print("Login successful!")
else:
    print("Invalid username or password.")

connection.close()