while True:
    print("Insert Red value")
    while True:
        Red = input()
        if int(Red) in range(0, 255):
            break
        else:
            print("Wrong value")

    print("Insert Green value")
    while True:
        Green = input()
        if int(Green) in range(0, 255):
            break
        else:
            print("Wrong value")
