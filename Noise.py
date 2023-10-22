from PIL import Image
import numpy as np

# Wczytaj obraz
image = Image.open("encoded.png")

# Konwertuj obraz do trybu RGBA (jeśli nie jest już w tym trybie)
image = image.convert("RGBA")

# Konwertuj obraz na tablicę NumPy
img_array = np.array(image)

# Wymiary obrazu
height, width, channels = img_array.shape

# Tworzenie szumu jako losowych liczb w zakresie od -25 do 25
noise = np.random.randint(-25, 25, (height, width, channels), dtype=np.int8)

# Dodaj szum do obrazu
noisy_image = np.clip(img_array + noise, 0, 255).astype(np.uint8)

# Utwórz obiekt Image z nowym obrazem
noisy_image = Image.fromarray(noisy_image)

# Zapisz lub wyświetl nowy obraz
noisy_image.show()
noisy_image.save("miau.png")
