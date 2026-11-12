# CodeAlpha_SecureCodingReview

Secure coding review of a demo Python login system (CodeAlpha Cyber Security Internship, Task 3).

## Contents

| File | Description |
|------|-------------|
| `login_system.py` | Original application (intentionally vulnerable to SQL injection) |
| `login_system_secure.py` | Fixed version using parameterized queries |
| `SECURITY_REPORT.md` | Full findings, proof of concept, fixes and recommendations |
| `screenshots/` | Evidence: attack before/after, Bandit results |

## How to run

```
python login_system.py
python login_system_secure.py
```

Test credentials for the demo database: `demo` / `password123`.

## Reproducing the vulnerability

Run `login_system.py` and enter:
```
Username: demo' --
Password: anything
```
The original prints "Login successful!". The secure version prints "Invalid username or password."

## Static analysis

```
pip install bandit
bandit login_system.py
bandit login_system_secure.py
```

## Summary

- **Critical:** SQL injection (f-string query), fixed with parameterized queries
- **High:** debug print leaking credentials (removed), plain text password storage (documented)
- See `SECURITY_REPORT.md` for the full list and remaining recommendations.

> This project is for educational purposes only.
