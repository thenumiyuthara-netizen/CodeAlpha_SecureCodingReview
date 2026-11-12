# Secure Coding Review: Demo Login System

**Internship:** CodeAlpha, Cyber Security, Task 3 (Secure Coding Review)
**Language:** Python 3 (sqlite3)
**Application audited:** `login_system.py`
**Fixed version:** `login_system_secure.py`

---

## 1. Overview

The audited application is a small console login system. It asks for a username and password, looks the user up in a SQLite database (`login_test.db`), and prints whether the login succeeded.

**Methods used**
- Manual code review (line by line)
- Static analysis with **Bandit**
- Dynamic testing with a crafted SQL injection payload
- Direct inspection of the database contents

---

## 2. Findings

| ID | Vulnerability | Location | Severity | Risk | Recommended fix |
|----|---------------|----------|----------|------|-----------------|
| 1 | **SQL Injection** (query built with an f-string) | `login_system.py`, line 18 | **Critical** | An attacker can log in without knowing the password, e.g. username `demo' --` | Use parameterized queries (`?` placeholders) |
| 2 | **Sensitive data exposure** (debug print of the full query, including the password) | line 20 | High | Credentials are written to the console and any logs | Remove debug output |
| 3 | **Plain text password storage** | database `users` table | High | Anyone with access to the DB file can read every password | Hash with a salted algorithm (bcrypt / PBKDF2) |
| 4 | **Weak / default credentials** (`demo` / `password123`) | database | Medium | Easily guessed | Enforce a password policy |
| 5 | **Password visible while typing** | line 15 | Medium | Shoulder surfing | Use `getpass.getpass()` |
| 6 | **No input validation** | lines 14-15 | Medium | Empty, oversized or malicious input is accepted | Validate length and content |
| 7 | **No brute-force protection** | whole login flow | Medium | Unlimited password guesses | Attempt limit / lockout |
| 8 | **No UNIQUE constraint on username** | table setup | Low | The `demo` user was inserted multiple times (duplicate rows) | `username TEXT UNIQUE` |
| 9 | **Connection not closed safely** | line 30 | Low | `close()` is skipped if an exception occurs | Use `try/finally` or a context manager |

---

## 3. Proof of Concept

### 3.1 Exploiting the vulnerable version (before the fix)

Input:
```
Enter username: demo' --
Enter password: anything
```

The generated query becomes:
```sql
SELECT * FROM users WHERE username = 'demo' --' AND password = 'anything'
```
The `--` turns the password check into a comment, so the query returns the `demo` row and the program prints **"Login successful!"** without a valid password.

Screenshot: `screenshots/01_vulnerable_attack.png`

### 3.2 Same payload against the fixed version (after the fix)

The same input is treated as a plain string, no user matches it, and the program prints **"Invalid username or password."**

Screenshot: `screenshots/02_secure_attack_blocked.png`

### 3.3 Legitimate login on the fixed version

`demo` / `password123` still logs in correctly, so the fix does not break normal behaviour.

Screenshot: `screenshots/03_secure_valid_login.png`

### 3.4 Plain text passwords in the database

Reading the `users` table shows passwords stored as readable text (`('demo', 'password123')`).

Screenshot: `screenshots/04_plaintext_passwords.png`

---

## 4. Static Analysis (Bandit)

Command:
```
bandit login_system.py
bandit login_system_secure.py
```

| File | Result |
|------|--------|
| `login_system.py` | Bandit reports a possible SQL injection (B608) for the string-built query |
| `login_system_secure.py` | The B608 issue is no longer reported |

Screenshots: `screenshots/05_bandit_before.png`, `screenshots/06_bandit_after.png`

---

## 5. Fixes Applied

**Before (vulnerable):**
```python
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
print(f"[DEBUG] Executing Query: {query}")
cursor.execute(query)
```

**After (fixed):**
```python
query = "SELECT * FROM users WHERE username = ? AND password = ?"
cursor.execute(query, (username, password))
```

- User input is passed as **data**, never as part of the SQL command, so injection is not possible.
- The debug print that leaked the query and password was removed.

---

## 6. Remaining Recommendations

The fixed version addresses the SQL injection and the debug leak. The following improvements are still recommended for a production system:

1. **Hash passwords** with a salt (bcrypt or PBKDF2) and compare hashes using a constant-time comparison.
2. Use **`getpass`** so the password is not echoed on screen.
3. Add **input validation** (non-empty, maximum length).
4. Add **attempt limiting / lockout** to slow down brute-force attacks.
5. Add a **UNIQUE constraint** on `username`.
6. Close the database connection with `try/finally`.
7. Enforce a **strong password policy** and remove default credentials.

---

## 7. Conclusion

The original application contained a **critical SQL injection vulnerability** that allowed authentication bypass, along with several secondary weaknesses such as plain text password storage and leaked debug output. Switching to parameterized queries removed the injection risk, which was verified by repeating the same attack against both versions and by re-running Bandit. Implementing the remaining recommendations would bring the application close to secure-coding best practice.
