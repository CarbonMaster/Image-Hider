from PIL import Image
import numpy as np
import hashlib

# Wczytaj obraz
image = Image.open('obraz.png')
image_array = np.array(image)

# Funkcja do szyfrowania i odszyfrowywania pojedynczej wartości
def encrypt_decrypt_value(value, password):
    # Utwórz instancję hasha na podstawie hasła
    hasher = hashlib.sha256(password.encode())
    
    # Przekształć hasło w łańcuch znaków o stałej długości (32 bajty)
    key = hasher.digest()
    
    # Szyfr XOR na bajcie
    encrypted_value = value ^ key[0]
    
    return encrypted_value

# Wprowadź hasło od użytkownika
password = input("Podaj hasło: ")

# Szyfruj obraz
encrypted_image_array = np.copy(image_array)

for i in range(4):
    encrypted_image_array[:, :, i] = np.vectorize(lambda x: encrypt_decrypt_value(x, password))(image_array[:, :, i])

# Odszyfruj obraz
decrypted_image_array = np.copy(encrypted_image_array)

for i in range(4):
    decrypted_image_array[:, :, i] = np.vectorize(lambda x: encrypt_decrypt_value(x, password))(encrypted_image_array[:, :, i])

# Utwórz obrazy zaszyfrowany i odszyfrowany
encrypted_image = Image.fromarray(encrypted_image_array)
decrypted_image = Image.fromarray(decrypted_image_array)

# Wyświetl obrazy
image.show(title='Oryginalny obraz')
encrypted_image.show(title='Zaszyfrowany obraz')
decrypted_image.show(title='Odszyfrowany obraz')
