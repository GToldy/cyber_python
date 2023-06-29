import random
import string


def generate_random_secret_key():
    secret_key = random.choices(string.ascii_lowercase, k=4)
    secret_key.extend(random.choices(string.ascii_uppercase, k=4))
    secret_key.extend(random.choices(string.digits, k=4))
    secret_key.extend(random.choices(string.punctuation, k=4))
    random.shuffle(secret_key)
    return secret_key
