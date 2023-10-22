from PIL import Image, ImageDraw
import numpy as np

# Wczytaj obrazy
image1 = Image.open("image1.png")
image2 = Image.open("image2.png")

image1.putalpha(255)
image2.putalpha(255)

image1 = image1.convert("L")
image2 = image2.convert("L")

# Pobierz dane pikseli z obrazow
pixels1 = list(image1.getdata())
pixels2 = list(image2.getdata())

# Porównaj rozmiary obrazów
width1, height1 = image1.size
width2, height2 = image2.size


#Jezeli obraz 1 jest wiekszy lub taki sam, wtedy
if width1 * height1 >= width2 * height2:
    #Obraz 2 jest wiadomoscia
    if width1>=width2 & height1>=height2:
        print("LOL")
    else:
        print("Images are not compatible to conversion")
elif width1 * height1 < width2 * height2:
    #Obraz 1 jest wiadomoscia
    modified_pixels = [round(7 * pixel / 255) for pixel in pixels1]
    modified_image_temp = Image.new("RGBA", image1.size)
    modified_image_temp.putdata(modified_pixels)

    red_channel = modified_image_temp.split()[0]
    modified_image_temp.putalpha(red_channel)

    new_image = Image.new("RGBA", modified_image_temp.size, (0, 0, 0, 0))
    new_image.putalpha(modified_image_temp.split()[3])
    #new_image.show()

    background = image2.convert("RGBA")
    top_image = new_image.convert("RGBA")
    
    bg_width, bg_height = background.size

    result = Image.new("RGBA", (bg_width, bg_height))
    result.paste(background, (0, 0))



    
    paste_x = (bg_width - top_image.width) // 2
    paste_y = (bg_height - top_image.height) // 2
    
    for y in range(top_image.height):
        for x in range(top_image.width):
            r_bg, g_bg, b_bg, a_bg = background.getpixel((paste_x + x, paste_y + y))
            
            r_top, g_top, b_top, a_top = top_image.getpixel((x, y))
            new_alpha = a_bg - a_top

            # Ensure the alpha value is within the 0-255 range
            new_alpha = max(0, min(255, new_alpha))

            # Set the new pixel in the result image
            result.putpixel((paste_x + x, paste_y + y), (r_bg, g_bg, b_bg, new_alpha))


    
    result.show()
    result.save("layered_image.png")


    

#Tutaj dokonuje odzyskania obrazu z tego gowna

image_converted = Image.open("layered_image.png")

width_o, height_o = image_converted.size

decoded_image = Image.new("RGBA", (width_o, height_o) )

pixels = list(image_converted.getdata())

min_alpha = 255 
max_alpha = 0

for pixel in pixels:
    temp = pixel[3]

    if temp < min_alpha:
        min_alpha = temp

    if temp > max_alpha:
        max_alpha = temp

temp = max_alpha - min_alpha

for x in range(width_o):
    for y in range(height_o):
        alpha_value = pixels[y * width_o + x][3]  # Odczytaj wartość alfa (A)

        if alpha_value < 255:
            alpha_value = 255 - alpha_value

        alpha_value = round(((alpha_value)/temp)*255)

        # Utwórz nowy piksel z wartością alfa i innymi kolorami na zero
        new_pixel = (alpha_value, alpha_value, alpha_value, 255)

        # Umieść nowy piksel w nowym obrazie na tych samych współrzędnych
        decoded_image.putpixel((x, y), new_pixel)

decoded_image.show()

