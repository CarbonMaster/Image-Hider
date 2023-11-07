from PIL import Image, ImageDraw
import numpy as np
import hashlib
import tkinter as tk
import random
import collections
from pyzbar.pyzbar import decode
import cv2
import qrcode
import string
#import sys
#sys.stdout.flush()
#from colorama import Fore, Back, Style, init

#init(autoreset=True)

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


null = None

def image_size(x_min, y_min):
    print(f"Insert image WIDTH value. Minimal is {x_min}")
    size1 = certain_value(x_min,0,1)
    print(f"Insert image HEIGHT value. Minimal is {y_min}")
    size2 = certain_value(y_min,0,1)
    return size1, size2

def certain_value(g1, g2, mode):
    #Mode 1 is making sure val is int. 2 is val in range of values
    while True:
        try:
            var = input()
            if mode == 1:
                if int(var) >= g1:
                    return var
                else:
                    print("Wrong value")
            if mode == 2:
                if int(var) in range(g1, g2+1):
                    return var
                else:
                    print("Wrong value")
        except:
            print("Wrong value")

def generate_random_string(length):
    letters = string.ascii_letters  # Możesz użyć `string.ascii_lowercase` lub `string.ascii_uppercase` lub `string.ascii_letters`
    result = ''.join(random.choice(letters) for _ in range(length))
    return result

def noise(image):
    print("Insert how many times do you want to noise disrupt the image")
    quant = get_value()
    i = 0
    while i in range(0,quant):
        img_array = np.array(image)
        height, width, channels = img_array.shape
        noise = np.random.randint(-25, 25, (height, width, channels - 1), dtype=np.int8)
        image = np.clip(img_array[:, :, :channels-1] + noise, 0, 255).astype(np.uint8)
        image = np.dstack((image, img_array[:, :, -1]))  # Zachowaj kanał alfa
        image = Image.fromarray(image)
        i += 1
    return image

def get_value():
    while True:
        try:
            quality = int(certain_value(0,255,2))
            break
        except:
            quality = None
            print("!!!Wrong value inserted. Try again.!!!")
    return quality

def define_image(img_name):
    print("\nInput image name and extention (ex. image.png), or press ENTER to abort")
    while True:
        try:
            if img_name is None:
                img_name = input()
                if img_name == "":
                    break
            test = Image.open(img_name)
            break
        except:
            img_name = None
            print("!!!Wrong type of name inserted. Try again.!!!")
    return test

def define_image_qr(img_name):
    print("\nInput image name and extention (ex. image.png)")
    while True:
        try:
            if img_name is None:
                img_name = input()
                if img_name == "" or img_name == None:
                    return img_name
            test = cv2.imread(img_name)
            break
        except:
            img_name = None
            print("!!!Wrong type of name inserted. Try again.!!!")
    return test


def show_image(image):
    print("Do you want to show output image? (y/n)")
    while True:
        anwser = input()
        if anwser == "y" or anwser == "Y":
            image.show(title='Image')
            break
        if anwser == "n" or anwser == "N":
            break
        else:
            print("!!!Incorrect anwser. Try again. Insert y for Yes or n for No.!!!")

def save_file(image):
    print("Call your output file (without extention),ENTER to skip saving, or CTRL + C to abort.")
    name = input()
    if name == "":
        return
    image.save(name+".png")
    print("")


def question():
    while True:
        anwser = input()
        if anwser == "y" or anwser == "Y":
            anw = True
            break
        if anwser == "n" or anwser == "N":
            anw = False
            break
        else:
            print("!!!Incorrect anwser. Try again. Insert y for Yes or n for No.!!!")
    return anw













def alpha_encode():
    #Inicjalizuje obrazy
    print("\nEncoding procedure.\nRemember, that smaller image will be encoded in the larger one, or the first in the second!\nTarget images have to be in current folder.\nYou don't require background picture for this encoding!")

    print("\nInput first image name and extention (ex. image1.png)")

    while True:
        try:
            img1_name = input()
            test = Image.open(img1_name)
            break
        except:
            print("Wrong type of name inserted. Try again.")
    
    print("\nInput second image name and extention (ex. image2.png), or press ENTER to create single color background")

    while True:
        try:
            img2_name = input()
            if img2_name != "":    
                test = Image.open(img2_name)
            else:
                print("Creating empty background...")
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
            print("Images are not compatible to conversion due to size limits")
    elif t_width1 * t_height1 < t_width2 * t_height2:
        #Obraz 1 jest wiadomoscia
        if t_width2>=t_width1 and t_height2>=t_height1:
            image1 = Image.open(img1_name)
            image2 = Image.open(img2_name)
            image3 = Image.open(img2_name)
        else:
            print("Images are not suitable to conversion due to size limits")
            
    if img2_name != "": 
        image2 = Image.open(img2_name)
    else:
        print("Do You want to set BACKGROUND color? (y/n) [White is default]")
        if question():
            print("Choose BACKGROUND color.")
            R,G,B = choose_color_val()
        else:
            R,G,B = 255,255,255
            
        print("Do You want to set background size? \nIf NO, size will be equal to MESSEAGE size (y/n)\n")
        if question():
            img_x, img_y = image_size(width1,height1)
            sizer = int(img_x), int(img_y)
            size_q = True
            image2 = Image.new("RGBA", sizer, (int(R), int(G), int(B), 255))
        else:
            image2 = Image.new("RGBA", image1.size, (int(R), int(G), int(B), 255))
        

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

    print("Insert value of image quality (from 0 to 255)")
    quality = get_value()
    
    modified_pixels = [round(quality * pixel / 255) for pixel in pixels1]
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

    print("Do you want to apply noise to whole output image? Reccomended for higher qualities of image! (y/n)")
    if question() == True:    
        result = noise(result)
    show_image(result)
    save_file(result)
    return

#Tutaj dokonuje odzyskania obrazu z tego gowna
def alpha_decode():
    image_converted = define_image(null)

    image_converted = image_converted.convert("RGBA")

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
    if temp == 0:
        temp=255

    for x in range(width_o):
        for y in range(height_o):
            alpha_value = pixels[y * width_o + x][3]  
            alpha_value = round(((255-alpha_value)/temp)*255)
            new_pixel = (alpha_value, alpha_value, alpha_value, 255)

            decoded_image.putpixel((x, y), new_pixel)
    #print(max_alpha)
    #print(min_alpha)
    #decoded_image.show()
    show_image(decoded_image)
    save_file(decoded_image)
    return










def scamble():
    print("\nChoose image to scramble. \n WARNING: Output image cannot be un-scrambled!")
    image = define_image(null)

    print("Input scramble seed text:")
    text = input()
    sha256_hash = hashlib.sha256(text.encode()).hexdigest()
    seed = int(sha256_hash, 16)
    print("Wartość SHA-256:", sha256_hash)
    print("Liczba całkowita na podstawie hasza:", seed)

    pixels = list(image.getdata())

    shuffled_pixels = random.sample(pixels, len(pixels))
    image.putdata(shuffled_pixels)

    show_image(image)
    save_file(image)
















def lsd():
    image = define_image(null)
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
    password = input("Podaj ziarno szyfrowania: ")

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


    show_image(encrypted_image)
    save_file(encrypted_image)







def calculate_coordinates(ID, width, height):
    ID -= 1  # ID jest numerowane od 1, a nie od 0
    x = ID // width
    y = ID % width
    return x, y

def hash_image():
    image = define_image(null)
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
            
    show_image(obraz)
    save_file(obraz)

    
    
    ilosc_cyfr = len(str(int(width)*int(height)))

    print("Input hash txt file name...")
    txt_name = (input() + ".txt")
    
    with open(txt_name, 'w') as plik:
        plik.write(f"{width}x{height};")
        for i in range(width):
            for j in range(height):
                format_id = str(output_data[i,j,0]).zfill(ilosc_cyfr)
                plik.write(format_id)
    print("")


def load_txt():
    print("\nInput hash txt file name")
    while True:
        try:
            txt_name = (input()+ ".txt")
            open(txt_name, 'r')
            break
        except:
            print("Wrong type of name inserted. Try again.")
    return txt_name


def hash_decrypt():
    
    encrypted_img = define_image(null)
    encrypted_img = encrypted_img.convert("RGBA")
    pixels = encrypted_img.load()

    decrypted_img = Image.new("RGBA", encrypted_img.size)
    txt_name = load_txt()
    with open(txt_name, 'r') as plik:
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

    show_image(decrypted_img)
    save_file(decrypted_img)

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
    id_to_indeks = {id_value: i for i, id_value in enumerate(liczby)}
    pixel_data_posortowana = sorted(pixel_data, key=lambda x: id_to_indeks[x["ID"]])
    uno = 0
    for x in range(width_enc):
        for y in range(height_enc):
            element = pixel_data_posortowana[uno]
            rgba = (element["R"], element["G"], element["B"], element["A"])
            encrypted_image.putpixel((x, y), rgba)
            uno = uno + 1

    show_image(encrypted_image)
    save_file(encrypted_image)














def hash_encrypt_short():
    print("Insert MESSEAGE image. Remember, that it has to be smaller or equal to BACKGROUND image!")
    image = define_image(null)
    image = image.convert("RGBA")
    pixels = image.load()

    print("Encoding...")

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
            
    #show_image(obraz)
    #save_file(obraz)

    
    
    ilosc_cyfr = len(str(int(width)*int(height)))

    print("Input hash txt file name...")
    txt_name = (input() + ".txt")
    
    with open(txt_name, 'w') as plik:
        plik.write(f"{width}x{height};")
        for i in range(width):
            for j in range(height):
                format_id = str(output_data[i,j,0]).zfill(ilosc_cyfr)
                plik.write(format_id)

    return obraz




def alpha_encrypt_short(image):
    #Inicjalizuje obrazy
    print("\nEncoding procedure.\nRemember, that smaller image will be encoded in the larger one, or the first in the second!\nTarget images have to be in current folder.")

    print("\nInput BACKGROUND image name and extention (ex. image1.png) OR press ENTER to create single color background")

    while True:
        try:
            img2_name = input()
            if img2_name != "":    
                test = Image.open(img2_name)
            else:
                print("Creating empty background...")
            break
        except:
            print("Wrong type of name inserted. Try again.")
    
    image1 = image
    width1, height1 = image1.size
    
    if img2_name != "": 
        image2 = Image.open(img2_name)
    else:
        print("Do You want to set BACKGROUND color? (y/n) [White is default]")
        if question():
            print("Choose BACKGROUND color.")
            R,G,B = choose_color_val()
        else:
            R,G,B = 255,255,255
            
        print("Do You want to set background size? \nIf NO, size will be equal to MESSEAGE size (y/n)\n")
        if question():
            img_x, img_y = image_size(width1,height1)
            sizer = int(img_x), int(img_y)
            size_q = True
            image2 = Image.new("RGBA", sizer, (int(R), int(G), int(B), 255))
        else:
            image2 = Image.new("RGBA", image1.size, (int(R), int(G), int(B), 255))
        
    
    width2, height2 = image2.size
    
    if width1>width2 or height1>height2:
        print("MESSEAGE image is larger than BACKGROUND! Aborting.")
        abort = True
        return image1, abort   

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

    print("Insert value of image quality (from 0 to 255)")
    quality = get_value()
    
    modified_pixels = [round(quality * pixel / 255) for pixel in pixels1]
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

    #print("Do you want to apply noise to whole output image? Reccomended for higher qualities of image! (y/n)")
    #if question() == True:    
    #    result = noise(result)
    #show_image(result)
    #save_file(result)
    abort = None
    return result, abort


def alpha_decode_short():
    image_converted = define_image(null)

    image_converted = image_converted.convert("RGBA")

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
    if temp == 0:
        temp=255

    for x in range(width_o):
        for y in range(height_o):
            alpha_value = pixels[y * width_o + x][3]  
            alpha_value = round(((255-alpha_value)/temp)*255)
            new_pixel = (alpha_value, alpha_value, alpha_value, 255)

            decoded_image.putpixel((x, y), new_pixel)
    #print(max_alpha)
    #print(min_alpha)
    #decoded_image.show()
    #show_image(decoded_image)
    #save_file(decoded_image)
    return decoded_image


def hash_decrypt_short(encrypted_img):

    encrypted_img = encrypted_img.convert("RGBA")
    pixels = encrypted_img.load()

   
    txt_name = load_txt()
    with open(txt_name, 'r') as plik:
        tresc = plik.read()

    

    width_dec, other = tresc.split("x")
    other_split = other.split(";")
    height_dec = int(other_split[0])
    width_dec = int(width_dec)
    liczba_str = other_split[1]
    width_re, height_re = encrypted_img.size

    if width_dec<width_re or height_dec<height_re:
        #Zrobic reakcje na wiekszy background niz obraz kodowany
        left = (width_re - width_dec) / 2
        top = (height_re - height_dec) / 2
        right = (width_re + width_dec) / 2
        bottom = (height_re + height_dec) / 2
        encrypted_img = encrypted_img.crop((left, top, right, bottom))

    decrypted_img = Image.new("RGBA", encrypted_img.size)
        
    
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

    return decrypted_img






def full_encrypt():
    messeage = hash_encrypt_short()
    print("Encoding alpha image...")
    result, abort = alpha_encrypt_short(messeage)
    if abort == True:
        return
    print("Do you want to apply noise to whole output image? Reccomended for higher qualities of image! (y/n)")
    if question() == True:    
        result = noise(result)
    show_image(result)
    save_file(result)  

    

def full_decrypt():
    print("Not ready yet.")
    print("\nAlpha decoding...")
    image = alpha_decode_short()
    print("Alpha decryption in progress.")
    dec_img = hash_decrypt_short(image)
    show_image(dec_img)
    save_file(dec_img)











def choose_color():
    while True:
        print("\nChoose FILL color for QR code.\n -1- White\n -2- Black\n -3- Red\n -4- Green\n -5- Blue\n -6- Define your own!(NON-FUNCTIONAL)\n")
        Input = input()
        if Input == "1":
            col1 = "white"
            break
        elif Input == "2":
            col1 = "black"
            break
        elif Input == "3":
            col1 = "red"
            break
        elif Input == "4":
            col1 = "green"
            break
        elif Input == "5":
            col1 = "blue"
            break
        elif Input == "6":
            print("Choose color values between 0 and 255!")
            R,G,B = choose_color_val()
            col1 = "#" + str(R) + str(G) + str(B)
            break
        else:
            you = generate_random_string(10)
            print(f"Wrong choice {you}!")
            Input = "0"
        break

    while True:
        print("\nChoose BACKGROUND color for QR code.\n -1- White\n -2- Black\n -3- Red\n -4- Green\n -5- Blue\n -6- Define your own! (NON-FUNCTIONAL)\n")
        Input = input()
        if Input == "1":
            col2 = "white"
            break
        elif Input == "2":
            col2 = "black"
            break
        elif Input == "3":
            col2 = "red"
            break
        elif Input == "4":
            col2 = "green"
            break
        elif Input == "5":
            col2 = "blue"
            break
        elif Input == "6":
            print("Choose color values between 0 and 255!")
            R,G,B = choose_color_val()
            col2 = "#" + str(R) + str(G) + str(B)
            break
        else:
            print("Wrong choice !")
            Input = "0"
        break
        
    
    return col1, col2

def choose_color_val():
    print("Insert Red value")
    R = certain_value(0,255,2)
    print("Insert Green value")
    G = certain_value(0,255,2)
    print("Insert Blue value")
    B = certain_value(0,255,2)
    return R, G, B



def split_data(data, max_length):
    data_blocks = []
    while data:
        data_block, data = data[:max_length], data[max_length:]
        data_blocks.append(data_block)
    return data_blocks

def qr_from_txt_encode(max_length):
    txt_name = load_txt()
    
    with open(txt_name, 'r') as plik:
        data_txt = plik.read()
        data = split_data(data_txt, max_length)

    while True:
        print("\nInput name for QR files, or press ENTER to cancel. Files will not be shown.")
        name = input()
        if name == "" or name == None:
            return
        break
    print("Encoding...")
    for i, data in enumerate(data):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        filename = f"{name}_{i+1}.png"
        img.save(filename)   

def qr_regular(data_to_encode):
    print("Encoding...")
    # Utwórz obiekt QRCode
    qr = qrcode.QRCode(
        version=1,  # Wersja kodu QR (może być dostosowana)
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Rodzaj korekcji błędów
        box_size=1,  # Rozmiar pojedynczego piksela (zależy od rozmiaru kodu QR)
        border=1,  # Margines w pikselach
    )

    # Dodaj dane do zakodowania
    qr.add_data(data_to_encode)
    qr.make(fit=True)

    col1, col2 = choose_color()
    
    # Tworzenie obiektu Image z kodem QR
    img = qr.make_image(fill_color=col1, back_color=col2)

    # Zapisz obraz kodu QR do pliku
    show_image(img)
    save_file(img)

def qr_encode():
    max_length = 4000
    print("Not ready yet.")
    
    print("\nChoose data to convert:\n -1- Written data\n -2- Txt file\n -3- Other file\n -back- Return\n\n WARNING: Input file cannot be more than 6,86 KB of size in written data!")
    print("(Or the image hash you may be trying to hide may not be higher than 1766 pixels in total, aprox. 50x32 pixels)\n")
    Input = input()
    while True:
        if Input == "1":
            print("\nInsert data to enter into QR code:\n")
            data_to_encode = input()
            qr_regular(data_to_encode)
            break
        elif Input == "2":
            qr_from_txt_encode(max_length)
            break
        elif Input == "3":
            print("Not ready yet.")
            break
        elif Input == "back":
            break
        else:
            print("!!!Wrong selection!!!")
            Input = "0"
    
 
    


def qr_decode():
    image = define_image_qr(None)
    if image=="" or image == None:
        return
    decoded_objects = decode(image)
    for obj in decoded_objects:
        print("Data:\n", obj.data)
    print("Do you want to save output data to .txt file? (y/n)")
    if question() == True:
        print("Input output txt file name...")
        txt_name = (input() + ".txt")
        with open(txt_name, 'w') as plik:
            plik.write(str(obj.data))
            print("File saved.")


def qr():
    while True:
        print("\nChoose what do You want to do with QR:\n -1- Encode an QR image\n -2- Read an QR image\n -3- Return to main menu\n")
        Input = input()
        if (Input == "1"):
            qr_encode()
        elif (Input == "2"):
            qr_decode()
        elif (Input == "3"):
            return
        else:
            print("!!!Wrong selection!!!")
            Input = "0"
        if "1" in Input or "2" in Input:
            print("\nOperation succesful. If you want to perform another action, enter it's number.")










def main():
    #root.mainloop()
    try:
        while True:
            print("\nInput desired operation number: ")
            print("\n 1 - Encode messeage in alpha\n 2 - Decode alpha messeeage\n 3 - Scramble an image")
            print(" 4 - Hash an image\n 5 - Dehash an image\n 6 - Full Encryption of Image\n 7 - Full decryption of Image")
            print(" 8 - Perform LSD on an Image\n 9 - QR Codes\n exit - Leave program")
            print("\n Or write 'help' for help!\n")
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
                hash_decrypt()
            elif (Input == "6"):
                full_encrypt()
            elif (Input == "7"):
                full_decrypt()
            elif (Input == "8"):
                lsd()
            elif (Input == "9"):
                qr()
            elif (Input == "exit"):
                break
            elif (Input == ("help")):
                print("yes, I can't help myself")
            else:
                print("!!!Wrong selection!!!")
                Input = "0"
            if "1" in Input or "2" in Input or "3" in Input or "4" in Input or "5" in Input or "6" in Input or "7" in Input or "8" in Input or "9" in Input:
                print("\nOperation succesful. If you want to perform another action, enter it's number.")
            
            
            
    except KeyboardInterrupt:
    #except error as e:
        print("Program failed or aborted")
        #print(f"{e}")
    return



main()


#NOTES:
#Usprawnić hash image

#To do:
#Zrobić elastyczność hasha na rozmiary większe i mniejsze
#Interfejs graficzny
#Zmniejszanie obrazu wyjściowego ma bazie braku kolorów

#Usunac zbedny shit
#Zrobic plik readme githubowy

#Zrobić klucz do losowego wstawiania pikseli

#po rozpoczeciu kazdego zadania lub podzadania musi byc \n

#Dodać pisanie wiadomości w formie pikselowych liter
#Rozmiar litery równy (7x4)[y/x]
#Przerwa mniedzy literami wynosi jedna kolumna bialych pikseli.
#Chcę zrobic program ktory bedzie konwertować wprowadzane znaki na pikselowe reprezentacje 7x5 które

#Ustalanie rozmiarów w kodzie QR
#wybieranie kolorów jest zjebane. kolory RGB z customowych kolorów nie zwracają wartości!
