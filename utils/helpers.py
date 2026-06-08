import random
import string


def generate_random_string(length):
    letters = string.ascii_lowercase
    random_string = "".join(random.choice(letters) for i in range(length))
    return random_string


def generate_random_number(length):
    numbers = "0123456789"
    random_number = "".join(random.choice(numbers) for i in range(length))
