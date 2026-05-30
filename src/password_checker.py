import re
import hashlib
import requests
from password_strength import PasswordStrength


def check_password(password: str) -> str | None:
    if len(password) < 8:
        return "Password is too short. It should be at least 8 characters long."
    if not re.search(r'[A-Z]', password):
        return "Password should contain at least one uppercase letter."
    if not re.search(r'[a-z]', password):
        return "Password should contain at least one lowercase letter."
    if not re.search(r'\d', password):
        return "Password should contain at least one digit."
    if not re.search(r'[!@#$%^&*()]', password):
        return "Password should contain at least one special character (e.g., !@#$%^&*())."
    return None


def check_hibp(password: str) -> tuple[bool, int]:
    """
    Checks the password against the HIBP Pwned Passwords API.
    Returns (pwned: bool, count: int).
    Uses k-anonymity — only the first 5 chars of the SHA-1 hash are sent.
    Raises requests.RequestException on network failure.
    """
    sha1 = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]

    response = requests.get(
        f"https://api.pwnedpasswords.com/range/{prefix}",
        timeout=5
    )
    response.raise_for_status()

    for line in response.text.splitlines():
        hash_suffix, count = line.split(":")
        if hash_suffix == suffix:
            return True, int(count)

    return False, 0


def get_strength(password: str) -> PasswordStrength:
    score = 0
    if len(password) >= 8:  score += 1
    if len(password) >= 12: score += 1
    if len(password) >= 16: score += 1
    
    if re.search(r'[A-Z]', password):        score += 1
    if re.search(r'[a-z]', password):        score += 1
    if re.search(r'\d', password):           score += 1
    if re.search(r'[!@#$%^&*()]', password): score += 1

    if score <= 2: return PasswordStrength.WEAK
    if score <= 4: return PasswordStrength.FAIR
    if score <= 5: return PasswordStrength.STRONG
    return PasswordStrength.VERY_STRONG