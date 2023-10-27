import cv2
from pyzbar.pyzbar import decode
def define_image_qr(img_name):
    print("\nInput image name and extention (ex. image.png)")
    while True:
        try:
            if img_name is None:
                img_name = input()
            test = cv2.imread(img_name)
            break
        except:
            img_name = None
            print("!!!Wrong type of name inserted. Try again.!!!")
    return test
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
def qr_decode():
    print("Not ready yet.")
    image = define_image_qr(None)
    decoded_objects = decode(image)
    for obj in decoded_objects:
        print("Data:\n", obj.data)
    print("Do you want to save output data to .txt file? (y/n)")
    if question() == True:
        print("Input output txt file name...")
        txt_name = (input() + ".txt")
        with open(txt_name, 'w') as plik:
            plik.write(str(obj.data))

qr_decode()
