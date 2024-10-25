import random
import string
from typing import List

# Generador código partida
def generate_code(n: int) -> str:
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(n))

def generate_unique_code(existing_codes: List[str]) -> str:
    new_code = generate_code(4)
    while new_code in existing_codes:
        new_code = generate_code
    return new_code

