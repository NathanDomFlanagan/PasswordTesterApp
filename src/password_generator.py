import secrets
import string


def generate_password(
    length: int = 16,
    use_upper: bool = True,
    use_lower: bool = True,
    use_digits: bool = True,
    use_special: bool = True
) -> str:
    """
    Generates a cryptographically secure password.
    Guarantees at least one character from each selected category.
    Raises ValueError if no character types are selected.
    """
    if not any([use_upper, use_lower, use_digits, use_special]):
        raise ValueError("At least one character type must be selected.")

    # Build the pool and guaranteed characters separately
    pool = ""
    guaranteed = []

    if use_upper:
        pool += string.ascii_uppercase
        guaranteed.append(secrets.choice(string.ascii_uppercase))

    if use_lower:
        pool += string.ascii_lowercase
        guaranteed.append(secrets.choice(string.ascii_lowercase))

    if use_digits:
        pool += string.digits
        guaranteed.append(secrets.choice(string.digits))

    if use_special:
        special_chars = "!@#$%^&*()"
        pool += special_chars
        guaranteed.append(secrets.choice(special_chars))

    # Fill remaining length from the full pool
    remaining = [secrets.choice(pool) for _ in range(length - len(guaranteed))]

    # Combine and shuffle so guaranteed chars aren't always at the start
    password_chars = guaranteed + remaining
    secrets.SystemRandom().shuffle(password_chars)

    return "".join(password_chars)