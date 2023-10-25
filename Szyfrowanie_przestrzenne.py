#NOTES:
#Generowany obraz na decode jest zjebany
#Kodowane ID są błędnie wybierane
#obraz w ogóle nie jest dekodowany. pokazuje obraz wejściowy!
#sprawdzić osie wstawiania pikseli!


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

    #Correct!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    start_number = 0
    for x in range(width_dec):
        for y in range(height_dec):
            pixel = encrypted_img.getpixel((x, y))
            red, green, blue, alpha = pixel
            pixel_data.append({"ID": liczby[start_number], "R": red, "G": green, "B": blue, "A": alpha})
            start_number = start_number + 1

#AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA


    #print(height_dec)
    
    


    #Sprawdzanie czy tabela powyzej ma duplikaty
    #unique_ids = set()
    #for data in pixel_data:
    #    ID_HUJ = data["ID"]
    #    if ID_HUJ in unique_ids:
    #        print(f"Znaleziono duplikat dla ID: {ID_HUJ}")
    #    else:
    #        unique_ids.add(ID_HUJ)

    
    


    #for tutaj in range(0,len(pixel_data)):
    #    pixel = pixel_data[tutaj]
    #    print("ID:", pixel["ID"])

    

    sorted_pixel_data = sorted(pixel_data, key=lambda x: x["ID"])

    #print(sorted_pixel_data[0])
    
    #moan = 0
    #for moan in range(0,len(sorted_pixel_data)):
    #    print(sorted_pixel_data[moan])


    decrypted_img_data = np.zeros((height_dec, width_dec, 5), dtype=int)
    
    #uno = 0
    #for x in range(width_dec):
    #    for y in range(height_dec):
    #        element = sorted_pixel_data[uno]
    #        decrypted_img_data[height_dec-1, width_dec-1, 0] = liczby[uno]
    #        decrypted_img_data[height_dec-1, width_dec-1, 1] = element["R"]
    #        decrypted_img_data[height_dec-1, width_dec-1, 2] = element["G"]
    #        decrypted_img_data[height_dec-1, width_dec-1, 3] = element["B"]
    #        decrypted_img_data[height_dec-1, width_dec-1, 4] = element["A"]
            #print(x, "   ", liczby[uno], "    ", uno)
    #        uno = uno + 1    


    #for pixel in sorted_pixel_data:
    #    x = pixel["ID"] % width_dec - 1
   #     y = pixel["ID"] // width_dec - 1
   #     rgba = (pixel["R"], pixel["G"], pixel["B"], pixel["A"])
   #     decrypted_img.putpixel((x, y), rgba)
        #pixel = pixel_data[tutaj]
        #print("ID:", pixel["ID"])

    uno = 0
    for y in range(width_dec):
        for x in range(height_dec):
            element = pixel_data[uno]
            rgba = (decrypted_img_data[height_dec-1, width_dec-1, 1], decrypted_img_data[height_dec-1, width_dec-1, 2], decrypted_img_data[height_dec-1, width_dec-1, 3], decrypted_img_data[height_dec-1, width_dec-1, 4])
            decrypted_img.putpixel((x, y), rgba)
            uno = uno + 1
            
    
    decrypted_img.show()
    #decrypted_img.save("obraz_decoded.png")
    

#BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
















def calculate_coordinates(ID, width, height):
    ID -= 1  # ID jest numerowane od 1, a nie od 0
    x = ID // width
    y = ID % width
    return x, y


def image_encrypt():
    image_name = "obraz.png"
    image = Image.open(image_name)
    image = image.convert("RGBA")
    pixels = image.load()

    obraz = Image.new("RGBA", image.size)
    obraz2 = Image.new("RGBA", image.size)

    width, height = image.size

    image_data = np.zeros((height, width, 1), dtype=int)
    output_data = np.zeros((height, width, 1), dtype=int)
    wolne = []

    id_counter = 1

    for i in range(width):
        for j in range(height):
            image_data[i, j, 0] = id_counter  # Unikatowy numer ID
            wolne.append(id_counter)
            id_counter = id_counter + 1
    
    #sus = []
    #sus.append(output_data[i,j,0])
    #for g in range(0,height):
    #        for h in range(0,width):
    #            sus.append(int(image_data[g,h,0]))
    #            #print(image_data[g,h,0])
    #duplikaty = False
    #kutas = 0
    #for kutas in range(0,len(sus)):
    #    if sus.count(kutas) > 1:
    #        duplikaty = True
    #        print(sus[kutas])
    #        break
    #print("IIIIIIIIIIIIIIIIIIIIIIIIIIII")
    #if duplikaty:
    #    print("Znaleziono duplikaty.")
    #else:
    #    print("XXXXXXXXXXXXXXXXXXXXXXXX")


    available_coordinates = [(x, y) for x in range(width) for y in range(height)]

    while wolne:
        rand_index = random.randrange(0,len(wolne))
        ID_choose = wolne[rand_index]
        #print(ID_choose)
        wolne.pop(rand_index)
        x, y = calculate_coordinates(ID_choose, width, height)
        #print(image_data[x,y,0])
        pixel_value = image.getpixel((x, y))

        random_index = random.randint(0, len(available_coordinates) - 1)
        random_cell = available_coordinates.pop(random_index)
        x_out, y_out = random_cell
        #available_coordinates.remove(random_cell)
        
        #x_out, y_out = available_coordinates.pop(rand_index)
        obraz.putpixel((x_out, y_out), pixel_value)
        output_data[x_out,y_out,0]=image_data[x, y, 0]

    for i in range(0,width):
            for j in range(0,height):
                pixel_value = image.getpixel((i, j))
                obraz2.putpixel((i, j), pixel_value)
            
    obraz.show()
    #obraz2.show()
    obraz.save("obraz_en.png")

    #for moan in range(0,len(output_data)):
    #        print(output_data[moan])

    
    
    
    with open('image_hash.txt', 'w') as plik:
        plik.write(f"{width}x{height};")
        for i in range(width):
            for j in range(height):
                format_id = str(output_data[i,j,0]).zfill(6)
                #print(output_data[i,j,0])
                #print(format_id)
                plik.write(format_id)

    #output_data_list = output_data.tolist()
    
    

def main():
    #image_encrypt()
    decrypt()
    
main()



#Zrobić klucz do losowego wstawiania pikseli
#renderowanie klucza-ID do pliku tekstowego
#zrobic klucz do identycznego rozkladania pikseli dla obrazow o identycznym rozmiarze


#Zamiarem tego kodu jest aby obraz wyjściowy był losowo rozpierdolony
#ale każdy piksel ma swoje ID na podstawie których można wstecznie ułożyć oryginalny obraz
#kodem odszyfrowującym jest lista numerów ID pikseli w obrazie.
#ilość maksymalną cyfr w ID można policzyć znając rozmiar obrazu.
