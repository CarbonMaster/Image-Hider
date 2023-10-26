#NOTES:
#Oh fuck yeah. It's all coming together.
#Wymiary optymalne są do 500x500 rozmiaru

#To do:
#Zrobić elastyczność hasha na rozmiary większe i mniejsze


from PIL import Image, ImageDraw
import numpy as np
import random
import collections


def find_ID_pixel(target_id):
    target_id = int(target_id)
    found = False
    for i in range(height):
        for j in range(width):
            if image_data[i, j, 0] == target_id:
                state = image_data[i, j, 1]
                print(f"ID: {target_id}, X: {i}, Y: {j}, Stan dodatkowy: {state}")
                found = True
                break
    if not found:
        print(f"Brak piksela o ID: {target_id} w obrazie.")
        

def decrypt():
    
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





def calculate_coordinates(ID, width, height):
    ID -= 1  # ID jest numerowane od 1, a nie od 0
    x = ID // width
    y = ID % width
    return x, y


def image_encrypt():
    image_name = "image1.png"
    image = Image.open(image_name)
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
    







def encrypt_with_txt():

    
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
    image_encrypt()
    decrypt()
    encrypt_with_txt()
    
main()



#Zrobić klucz do losowego wstawiania pikseli
#renderowanie klucza-ID do pliku tekstowego
#zrobic klucz do identycznego rozkladania pikseli dla obrazow o identycznym rozmiarze


#Zamiarem tego kodu jest aby obraz wyjściowy był losowo rozpierdolony
#ale każdy piksel ma swoje ID na podstawie których można wstecznie ułożyć oryginalny obraz
#kodem odszyfrowującym jest lista numerów ID pikseli w obrazie.
#ilość maksymalną cyfr w ID można policzyć znając rozmiar obrazu.
#dodac generowanie txt z hashem dla podanego rozmiaru obrazu, bez jego generowania
