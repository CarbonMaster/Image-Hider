from PIL import Image, ImageDraw
import numpy as np
import hashlib
import tkinter as tk
import random
import collections

#root = tk.Tk()
#root.title("Moja aplikacja")

#button = tk.Button(root, text="Kliknij mnie")
#button.pack()  # Dodaj przycisk do okna

#label = tk.Label(root, text="To jest etykieta")
#label.pack()

#entry = tk.Entry(root)
#entry.pack()

#checkbox = tk.Checkbutton(root, text="Zaznacz mnie")
#checkbox.pack()

def on_button_click():
    label.config(text="Naciśnięto przycisk")

#button = tk.Button(root, text="Kliknij mnie", command=on_button_click)

#hasher = hashlib.sha256()

#Główna pętla programu




def define_image():
    while True:
        try:
            img_name = input()
            test = Image.open(img_name)
            break
        except:
            print("Wrong type of name inserted. Try again.")
    return test







def alpha_encode():
    #Inicjalizuje obrazy
    print("\nEncoding procedure.\nRemember, that smaller image will be encoded in the larger one, or the first in the second!\nTarget images have to be in current folder.")

    print("\nInput first image name and extention (ex. image1.png)")

    while True:
        try:
            img1_name = input()
            test = Image.open(img1_name)
            break
        except:
            print("Wrong type of name inserted. Try again.")
    
    print("\nInput second image name and extention (ex. image2.png)")

    while True:
        try:
            img2_name = input()
            test = Image.open(img2_name)
            break
        except:
            print("Wrong type of name inserted. Try again.")
    
    t_image1 = Image.open(img1_name)
    t_image2 = Image.open(img2_name)
    t_width1, t_height1 = t_image1.size
    t_width2, t_height2 = t_image2.size
    
    
    if t_width1 * t_height1 >= t_width2 * t_height2:
        #Obraz 2 jest wiadomoscia
        if t_width1>=t_width2 and t_height1>=t_height2:
            image2 = Image.open(img1_name)
            image1 = Image.open(img2_name)
            image3 = Image.open(img1_name)
        else:
            print("Images are not compatible to conversion due to size limits (uno)")
    elif t_width1 * t_height1 < t_width2 * t_height2:
        #Obraz 1 jest wiadomoscia
        if t_width2>=t_width1 and t_height2>=t_height1:
            image1 = Image.open(img1_name)
            image2 = Image.open(img2_name)
            image3 = Image.open(img2_name)
        else:
            print("Images are not suitable to conversion due to size limits (dos)")
            
    print("Do you want to show output image? (y/n)")
    show = False
    while True:
        anwser = input()
        if anwser == "y" or anwser == "Y":
            show_img = True
            break
        if anwser == "n" or anwser == "N":
            show_img = False
            break
        else:
            print("Incorrect anwser. Try again. Insert y for Yes or n for No.")

    print("Encoding...") 

    image1 = image1.convert("RGBA")
    #image2 = image2.convert("RGB")
    image2 = image2.convert("RGBA")
    
    pixels1 = image1.load()
    pixels2 = image2.load()

    width_1, height_1 = image1.size
    for x in range(width_1):
        for y in range(height_1):
            r, g, b, a = pixels1[x, y]
            a = 255  # Ustaw kanał alfa na maksymalną wartość (255)
            pixels1[x, y] = (r, g, b, a)

    width_2, height_2 = image2.size
    #for x in range(width_2):
        #for y in range(height_2):
            #r, g, b, a = pixels2[x, y]
            #a = 255  # Ustaw kanał alfa na maksymalną wartość (255)
            #pixels2[x, y] = (r, g, b, a)

    for x in range(width_1):
        for y in range(height_1):
            r, g, b, a = pixels1[x, y]
            r = round(r * (a / 255))
            g = round(g * (a / 255))
            b = round(b * (a / 255))
            pixels1[x, y] = (r, g, b, a)    
    
    
    image1 = image1.convert("L")

    # Pobierz dane pikseli z obrazow
    pixels1 = list(image1.getdata())
    pixels2 = list(image2.getdata())

    # Porównaj rozmiary obrazów
    width1, height1 = image1.size
    width2, height2 = image2.size

    modified_pixels = [round(100 * pixel / 255) for pixel in pixels1]
    modified_image_temp = Image.new("RGBA", image1.size)
    modified_image_temp.putdata(modified_pixels)

    red_channel = modified_image_temp.split()[0]
    modified_image_temp.putalpha(red_channel)

    new_image = Image.new("RGBA", modified_image_temp.size, (0, 0, 0, 0))
    new_image.putalpha(modified_image_temp.split()[3])

    image2.putalpha(255)
    background = image2.convert("RGBA")

    white_background = Image.new("RGBA", image2.size)

    for y in range(white_background.height):
        for x in range(white_background.width):
            r_bg, g_bg, b_bg, a_bg = background.getpixel((x,y))
            white_background.putpixel((x,y),(r_bg, g_bg, b_bg, 255))        
    
    top_image = new_image.convert("RGBA")
    
    bg_width, bg_height = white_background.size

    result = Image.new("RGBA", (bg_width, bg_height))
    result.paste(white_background, (0, 0))
    
    paste_x = (bg_width - top_image.width) // 2
    paste_y = (bg_height - top_image.height) // 2
    
    for y in range(top_image.height):
        for x in range(top_image.width):
            r_bg, g_bg, b_bg, a_bg = white_background.getpixel((paste_x + x, paste_y + y))
            r_top, g_top, b_top, a_top = top_image.getpixel((x, y))
            new_alpha = a_bg - a_top
            new_alpha = max(0, min(255, new_alpha))
            result.putpixel((paste_x + x, paste_y + y), (0, 0, 0, new_alpha))

    for y in range(background.height):
        for x in range(background.width):
            r_bg, g_bg, b_bg, a_bg = white_background.getpixel((x,y))
            #if r_bg==0 and g_bg==0 and b_bg ==0:
            #    r_bg=255
            #    g_bg=255
            #    b_bg=255

            r_res, g_res, b_res, a_res = result.getpixel((x, y))

            result.putpixel((x,y), (r_bg, g_bg, b_bg, a_res))
            
    #result = noise(result)
    if show_img == True:
        result.show()

        
    print("Call your output file (without extention), or press CTRL + C to abort.")
    
    result.save(input()+".png")
    
    return

#Tutaj dokonuje odzyskania obrazu z tego gowna
def alpha_decode():
    image_converted = Image.open("encoded.png")

    width_o, height_o = image_converted.size

    decoded_image = Image.new("RGBA", (width_o, height_o) )

    pixels = list(image_converted.getdata())

    min_alpha = 255 
    max_alpha = 255

    for pixel in pixels:
        temp = pixel[3]

        if temp < min_alpha and temp > 0:
            min_alpha = temp

    temp = max_alpha - min_alpha

    for x in range(width_o):
        for y in range(height_o):
            alpha_value = pixels[y * width_o + x][3]  
            alpha_value = round(((255-alpha_value)/temp)*255)
            new_pixel = (alpha_value, alpha_value, alpha_value, 255)

            decoded_image.putpixel((x, y), new_pixel)
    #print(max_alpha)
    print(min_alpha)
    #decoded_image.show()
    decoded_image.save("decoded.png")
    return










def scamble():
    print("Input name of image to scramble:")
    while True:
        try:
            name = input()
            image = Image.open(name)
            break
        except:
            print("Wrong type of name inserted. Try again.")
    print("Input scramble seed text:")
    text = input()
    sha256_hash = hashlib.sha256(text.encode()).hexdigest()
    seed = int(sha256_hash, 16)
    print("Wartość SHA-256:", sha256_hash)
    print("Liczba całkowita na podstawie hasza:", seed)

    pixels = list(image.getdata())

    shuffled_pixels = random.sample(pixels, len(pixels))
    image.putdata(shuffled_pixels)

    # Zapisz obraz
    image.show()







def noise(image):
    #image = image.convert("RGBA")
    img_array = np.array(image)
    height, width, channels = img_array.shape
    noise = np.random.randint(-25, 25, (height, width, channels), dtype=np.int8)
    noisy_image = np.clip(img_array + noise, 0, 255).astype(np.uint8)
    noisy_image = Image.fromarray(noisy_image)
    #noisy_image.show()
    #noisy_image.save("miau.png")
    return noisy_image








def lsd():
    image = define_image()
    image = image.convert("RGBA")
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
    #image.show(title='Oryginalny obraz')
    encrypted_image.show(title='Zaszyfrowany obraz')
    #decrypted_image.show(title='Odszyfrowany obraz')







def calculate_coordinates(ID, width, height):
    ID -= 1  # ID jest numerowane od 1, a nie od 0
    x = ID // width
    y = ID % width
    return x, y

def hash_image():
    print("\nInput image name and extention (ex. image1.png)")
    image = define_image()
    #image = Image.open(image_name)
    image = image.convert("RGBA")
    pixels = image.load()

    obraz = Image.new("RGBA", image.size)
    obraz2 = Image.new("RGBA", image.size)

    width, height = image.size

    image_data = np.zeros((width, height, 1), dtype=int)
    output_data = np.zeros((width, height, 1), dtype=int)
    wolne = []

    id_counter = 1

    for i in range(0,width):
        for j in range(0,height):
            #print(j)
            image_data[i, j, 0] = id_counter  # Unikatowy numer ID
            wolne.append(id_counter)
            id_counter = id_counter + 1


    available_coordinates = [(x, y) for x in range(width) for y in range(height)]

    while wolne:
        rand_index = random.randrange(0,len(wolne))
        ID_choose = wolne[rand_index]
        wolne.pop(rand_index)
        y, x = calculate_coordinates(ID_choose, width, height)
        pixel_value = image.getpixel((x, y))

        random_index = random.randint(0, len(available_coordinates) - 1)
        random_cell = available_coordinates.pop(random_index)
        x_out, y_out = random_cell
        obraz.putpixel((x_out, y_out), pixel_value)
        output_data[x_out,y_out,0]=image_data[x, y, 0]
            
    obraz.show()
    obraz.save("obraz_en.png")

    
    
    ilosc_cyfr = len(str(int(width)*int(height)))
    
    with open('image_hash.txt', 'w') as plik:
        plik.write(f"{width}x{height};")
        for i in range(width):
            for j in range(height):
                format_id = str(output_data[i,j,0]).zfill(ilosc_cyfr)
                plik.write(format_id)

def hash_decrypt():
    
    image_name = "obraz_en.png"
    encrypted_img = Image.open(image_name)
    encrypted_img = encrypted_img.convert("RGBA")
    pixels = encrypted_img.load()

    decrypted_img = Image.new("RGBA", encrypted_img.size)

    with open('image_hash.txt', 'r') as plik:
        tresc = plik.read()

    width_dec, other = tresc.split("x")
    other_split = other.split(";")
    height_dec = int(other_split[0])
    width_dec = int(width_dec)
    liczba_str = other_split[1]
    
    hash = str(liczba_str)  # Konwersja liczby na łańcuch znaków
    ilosc_cyfr = len(str(int(width_dec)*int(height_dec)))
    
    
    # Pętla do rozdzielania ciągu na liczby
    liczby = []
    for i in range(0, len(hash), ilosc_cyfr):
        liczba = hash[i:i + ilosc_cyfr]
        liczby.append(int(liczba))
        #print(int(liczba))

    pixel_data = []
    start_number = 0
    for x in range(width_dec):
        for y in range(height_dec):
            pixel = encrypted_img.getpixel((x, y))
            red, green, blue, alpha = pixel
            pixel_data.append({"ID": liczby[start_number], "R": red, "G": green, "B": blue, "A": alpha})
            start_number = start_number + 1

    sorted_pixel_data = sorted(pixel_data, key=lambda x: x["ID"])

    uno = 0
    for x in range(width_dec):
        for y in range(height_dec):
            element = sorted_pixel_data[uno]
            rgba = (element["R"], element["G"], element["B"], element["A"])
            decrypted_img.putpixel((x, y), rgba)
            uno = uno + 1
            
    
    decrypted_img.show()
    decrypted_img.save("obraz_decoded.png")

def hash_with_txt():
    image_name = "image1.png"
    base_image = Image.open(image_name)
    base_image = base_image.convert("RGBA")
    pixels = base_image.load()

    encrypted_image = Image.new("RGBA", base_image.size)

    with open('image_hash.txt', 'r') as plik:
        tresc = plik.read()

    width_enc, other = tresc.split("x")
    other_split = other.split(";")
    height_enc = int(other_split[0])
    width_enc = int(width_enc)
    liczba_enc = other_split[1]

    width, height = base_image.size

    if width!=width_enc or height!=height_enc:
        print("Image is not size compatible with hash!")
        return

    hash = str(liczba_enc)
    ilosc_cyfr = len(str(int(width_enc)*int(height_enc)))
    
    # Pętla do rozdzielania ciągu na liczby
    liczby = []
    for i in range(0, len(hash), ilosc_cyfr):
        liczba = hash[i:i + ilosc_cyfr]
        liczby.append(int(liczba))
    pixel_data = []
    start_number = 1
    for x in range(width_enc):
        for y in range(height_enc):
            pixel = base_image.getpixel((x, y))
            red, green, blue, alpha = pixel
            pixel_data.append({"ID": start_number, "R": red, "G": green, "B": blue, "A": alpha})
            start_number = start_number + 1
    #indeksy_sortowania = sorted(range(len(liczby)), key=lambda x: liczby[x])
    #pixel_data_posortowana = [pixel_data[i] for i in indeksy_sortowania]

    id_to_indeks = {id_value: i for i, id_value in enumerate(liczby)}
    pixel_data_posortowana = sorted(pixel_data, key=lambda x: id_to_indeks[x["ID"]])

    #print(pixel_data[1])
    #print(pixel_data_posortowana[1])
    #print(liczby[1])

    uno = 0
    for x in range(width_enc):
        for y in range(height_enc):
            element = pixel_data_posortowana[uno]
            rgba = (element["R"], element["G"], element["B"], element["A"])
            encrypted_image.putpixel((x, y), rgba)
            uno = uno + 1
    encrypted_image.show()
    encrypted_image.save("image_encrypted_txt.png")










def main():
    #root.mainloop()
    try:
        while True:
            print("\nInput desired operation number: ")
            print("\n 1 - Encode messeage in alpha\n 2 - Decode alpha messeeage\n 3 - Scramble an image")
            print(" 4 - Hash an image\n 5 - Dehash an image\n 6 - Full Encryption of Image\n 7 - Full decryption of Image")
            print(" 8 - Perform LSD on an Image\n 9 - Leave program")
            print("\n Or write 'help' for help!")
            Input = input()
            if (Input == "1"):
                alpha_encode()
            elif (Input == "2"):
                alpha_decode()
            elif (Input == "3"):
                scamble()
            elif (Input == "4"):
                hash_image()
            elif (Input == "5"):
                break
            elif (Input == "6"):
                break
            elif (Input == "7"):
                break
            elif (Input == "8"):
                lsd()
            elif (Input == "9"):
                break
            elif (Input == ("help")):
                print("yes, I can't help myself")
            else:
                print("Wrong selection!")
            if (Input == ("1" or "2" or "3")):
                print("\nOperation succesful. If you want to perform another action, enter it's number.")
            Input = 0
            
            

    except:
        print("Program failed or aborted")
    return



main()


#NOTES:
#Oh fuck yeah. It's all coming together.
#Wymiary optymalne są do 500x500 rozmiaru

#To do:
#Zrobić elastyczność hasha na rozmiary większe i mniejsze

#LEft to do:
#Interfejs graficzny
#Określanie które obrazy do konwersji
#Dodatkowe utrudnienie w dostrzeżeniu szyfrowania poprzez dodanie wachań wartości kolorów
#Zmniejszanie obrazu wyjściowego ma bazie braku kolorów
#Dodać kodowanie na background jako pusty obraz, rozmiarowo identyczny jak wiadomość
#

#Usunac zbedny shit
#wstawianie dokladnosci kodowanego obrazu
#połączyć program przestrzenny z tym
#Zrobic plik readme githubowy
#Dodac obsluge przerwac aby CTRL+C wylaczal program

#Zrobić klucz do losowego wstawiania pikseli
#renderowanie klucza-ID do pliku tekstowego
#zrobic klucz do identycznego rozkladania pikseli dla obrazow o identycznym rozmiarze


#Zamiarem tego kodu jest aby obraz wyjściowy był losowo rozpierdolony
#ale każdy piksel ma swoje ID na podstawie których można wstecznie ułożyć oryginalny obraz
#kodem odszyfrowującym jest lista numerów ID pikseli w obrazie.
#ilość maksymalną cyfr w ID można policzyć znając rozmiar obrazu.
#dodac generowanie txt z hashem dla podanego rozmiaru obrazu, bez jego generowania


