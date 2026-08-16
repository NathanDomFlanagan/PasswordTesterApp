# Password Tester

A desktop password strength checker and generator, built with Python and [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter). Checks passwords against both local complexity rules and the [Have I Been Pwned](https://haveibeenpwned.com/) breach database using k-anonymity, and generates cryptographically secure passwords.

## Features

**Test tab**
- Live strength meter as you type (Weak / Fair / Strong / Very Strong), based on length and character variety
- Complexity validation — flags missing uppercase, lowercase, digits, or special characters
- **Have I Been Pwned check** — looks up the password against real-world breach data without ever sending the actual password over the network (see "How the HIBP check works" below)
- Show/hide password toggle
- Light/dark theme toggle
- "Show Tips" popup with password best practices

**Generate tab**
- Adjustable length via slider (8–32 characters)
- Toggle which character types to include (uppercase, lowercase, digits, special characters)
- Guarantees at least one character from each selected type, cryptographically shuffled — not a naive random pick that could miss a required category
- One-click copy to clipboard

## How the HIBP check works

Your actual password is never sent anywhere. The app hashes it locally with SHA-1, then sends only the **first 5 characters** of that hash to the Pwned Passwords API. The API returns every breached hash sharing that prefix, and the match against the remaining hash suffix happens locally on your machine. This is the same k-anonymity model HIBP itself recommends — the full password (or even its full hash) never leaves your computer.

The check runs on a background thread so the UI doesn't freeze while waiting on the network request.

## Requirements

- Python 3.10+ (uses the `str | None` union type syntax)
- [`customtkinter`](https://pypi.org/project/customtkinter/)
- [`requests`](https://pypi.org/project/requests/)

```bash
pip install customtkinter requests
```

## Running it

```bash
cd src
python main.py
```

## Project structure

| File | Purpose |
|---|---|
| `main.py` | Entry point — creates and runs the app window |
| `password_tester_app.py` | All UI: the CustomTkinter window, both tabs, and the logic wiring buttons/inputs to the checker and generator |
| `password_checker.py` | `check_password()` (local complexity rules), `check_hibp()` (breach-database lookup via k-anonymity), `get_strength()` (scores a password into a `PasswordStrength` level) |
| `password_generator.py` | `generate_password()` — builds a cryptographically secure password using Python's `secrets` module, guaranteeing at least one character from each selected category |
| `password_strength.py` | `PasswordStrength` enum (`WEAK`, `FAIR`, `STRONG`, `VERY_STRONG`) |

## Password rules

A password is flagged as insecure by `check_password()` if it's missing any of:
- At least 8 characters
- One uppercase letter
- One lowercase letter
- One digit
- One special character from `!@#$%^&*()`

The strength meter (`get_strength()`) scores more granularly — length beyond 8 characters (12, 16+) and character variety both add to the score, giving a smoother Weak → Very Strong gradient rather than a strict pass/fail.

## Notes

- Requires an internet connection for the breach-database check; if the request fails (no connection, API down), the app shows a neutral "could not reach breach database" message rather than blocking the rest of the results.