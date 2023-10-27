import random
import string

def generate_random_string(length):
    letters = string.ascii_letters  # Możesz użyć `string.ascii_lowercase` lub `string.ascii_uppercase` lub `string.ascii_letters`
    result = ''.join(random.choice(letters) for _ in range(length))
    return result

# Wygeneruj losowy ciąg liter o długości 10
random_string = generate_random_string(10)
print(random_string)
