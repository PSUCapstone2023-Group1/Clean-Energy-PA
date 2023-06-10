import random
import string


def generate_username(length=8):
    # Generate a random username with the given length
    username = "".join(random.choices(string.ascii_lowercase + string.digits, k=length))
    return username


def generate_email(domain="example.com", length=8):
    # Generate a random email address
    username = generate_username(length)
    email = f"{username}@{domain}"
    return email


def generate_password(length=12):
    # Define a pool of allowed characters for the password
    characters = string.ascii_letters + string.digits + string.punctuation

    # Generate a random password with the given length
    password = "".join(random.choice(characters) for _ in range(length))
    return password


def generate_name(length=5):
    # Generate a random name with the given length
    username = "".join(random.choices(string.ascii_lowercase + string.digits, k=length))
    return username


def generate_zip_code(is_valid):
    if is_valid:
        return "90210"
    else:
        return "000000"
