import re
import string
import random

def password_strength(password):
    score = 0

    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1
    if len(password) >= 17:
        score += 1

    if re.search(r'[A-Z]', password):
        score += 1

    if re.search(r'[a-z]', password):
        score += 1

    if re.search(r'[0-9]', password):
        score += 1

    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 1

    return score

def password_generator(n):
    uppercase_letters = string.ascii_uppercase
    lowercase_letters = string.ascii_lowercase
    digits = string.digits
    special_characters = string.punctuation

    # Combine all character sets
    all_characters = uppercase_letters + lowercase_letters + digits + special_characters

    # Ensure at least one character from each set is included
    password = [random.choice(uppercase_letters),
                random.choice(lowercase_letters),
                random.choice(digits),
                random.choice(special_characters)]

    # Fill the remaining length of the password randomly from all character sets
    password.extend(random.choice(all_characters) for _ in range(n - 4))

    # Shuffle the password characters to ensure randomness
    random.shuffle(password)

    # Convert the list of characters to a string
    return ''.join(password)

    
