import random


def generate_hex_id(length=12):
    chars = "0123456789abcdef"
    id = "".join(random.choice(chars) for _ in range(length))

    return id
