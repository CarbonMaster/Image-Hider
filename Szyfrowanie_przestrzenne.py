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
    image_name = "obraz.png"
    encrypted_img = Image.open(image_name)
    encrypted_img = encrypted_img.convert("RGBA")
    pixels = encrypted_img.load()

    decrypted_img = Image.new("RGBA", encrypted_img.size)



    

    #Rozbijanie ciągu cyfr na zestawy ID (z odczytem listy ID)

    with open('ID_list.txt', 'r') as plik:
        dlugi_ciag_cyfr = plik.read()

    #Ma znajdywac tą ilosc cyfr w liczbie

    #Musi jakoś weryfikować jaki rozmiar ma obraz
    #Np kod_ID moze miec pierwsze wartosci temu rowne

    #liczba = width * height
    liczba_str = str(liczba)  # Konwersja liczby na łańcuch znaków
    ilosc_cyfr = len(liczba_str)

    #(dodatkowo)
    ilosc_cyfr = 4

    liczby = []  # Lista, w której będziemy przechowywać rozdzielone liczby

    # Pętla do rozdzielania ciągu na liczby
    for i in range(0, len(dlugi_ciag_cyfr), ilosc_cyfr_w_liczbie):
        liczba = dlugi_ciag_cyfr[i:i + ilosc_cyfr_w_liczbie]
        liczby.append(int(liczba))

    print(liczby)



def image_encrypt():
    image_name = "obraz.png"
    image = Image.open(image_name)
    image = image.convert("RGBA")
    pixels = image.load()

    obraz = Image.new("RGBA", image.size)

    width, height = image.size

    image_data = np.zeros((height, width, 2), dtype=int)
    output_data = np.zeros((height, width, 1), dtype=int)
    wolne = []





    # Utwórz kolejkę dwuwymiarową jako listę kolejek (np. 3x3)
    wymiar_x = 3
    wymiar_y = 3
    wymiar_z = 3
    kolejka = [[[collections.deque() for _ in range(width)] for _ in range(height)] for _ in range(2)]

    # Dodaj element do kolejki na konkretnej pozycji (x, y)
    element = 42
    x = 1
    y = 2
    #kolejka_dwuwymiarowa[y][x].append(element)

    # Usuń element z konkretnej pozycji (x, y)
    #usuniety_element = kolejka_dwuwymiarowa[y][x].popleft()
    
    




    id_counter = 1

    for i in range(height):
        for j in range(width):
            image_data[i, j, 0] = id_counter  # Unikatowy numer ID
            wolne.append(id_counter)
            image_data[i, j, 1] = 0  # Stan dodatkowy początkowo ustawiony na 0
            id_counter += 1

    mucio=0
    length_left = len(wolne)
    while length_left>0:
        ID_choose = random.choice(wolne)

        x = ((ID_choose) % height)
        y = (ID_choose ) // width

        print(x)
        print(y)
        
        print(ID_choose)
        #pixel_value = image.getpixel((121, 121))
        #obraz.putpixel((x, y), pixel_value)

        #ten sposób usuwania jest wolny w chuj
        wolne.remove(ID_choose)
        #print(image_data[x, y, 0])
        mucio = mucio + 1
        length_left = length_left - 1
        if mucio > 10000:
            #print(len(wolne))
            mucio = 0


    print(wolne)
            
    obraz.show()
    print(random.choice(wolne))
    image_data[x, y, 1] = 1
    

def main():
    image_encrypt()

main()



#Zrobić klucz do losowego wstawiania pikseli
#renderowanie klucza-ID do pliku tekstowego
#zrobic klucz do identycznego rozkladania pikseli dla obrazow o identycznym rozmiarze


#Zamiarem tego kodu jest aby obraz wyjściowy był losowo rozpierdolony
#ale każdy piksel ma swoje ID na podstawie których można wstecznie ułożyć oryginalny obraz
#kodem odszyfrowującym jest lista numerów ID pikseli w obrazie.
#ilość maksymalną cyfr w ID można policzyć znając rozmiar obrazu.
