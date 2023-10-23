from PIL import Image, ImageDraw
import hashlib
import random

text = "Przykładowy tekst"
sha256_hash = hashlib.sha256(text.encode()).hexdigest()
seed = int(sha256_hash, 16)
print("Wartość hasza SHA-256:", sha256_hash)
print("Liczba całkowita na podstawie hasza:", seed)

image = Image.open("image4.png")
pixels = list(image.getdata())

shuffled_pixels = random.sample(pixels, len(pixels))
image.putdata(shuffled_pixels)

# Zapisz obraz
image.show()
