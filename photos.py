from PIL import Image
from os import listdir
from os.path import isfile, join

onlyfiles = [f for f in listdir("/Users/gerardo/PycharmProjects/processing/venv/Photos") if isfile(join("/Users/gerardo/PycharmProjects/processing/venv/Photos", f))]
file = open("Fotos_info.txt", "w")

for i in range(len(onlyfiles)):
    if onlyfiles[i] != ".DS_Store":
        print(onlyfiles[i])
        img = Image.open("Photos/" + onlyfiles[i])
        print("Image " + str(i + 1))
        dict = img._getexif()

        if dict is not None:
            data = img._getexif().get(34853)
            if data is not None:
                # file.write("Nombre archivo: " + onlyfiles[i] + "\n")
                # file.write("Fecha: " + str(img._getexif()[306]) + "\n")
                # file.write("latitud: " + str(img._getexif()[34853][2][0][0]) + "° " + str(img._getexif()[34853][2][1][0]) + "' " + str(img._getexif()[34853][2][2][0]/img._getexif()[34853][2][2][1]) + "'' " + img._getexif()[34853][1] + "\n")
                # file.write("longitud: " + str(img._getexif()[34853][4][0][0]) + "° " + str(img._getexif()[34853][4][1][0]) + "' " + str(img._getexif()[34853][4][2][0]/img._getexif()[34853][4][2][1]) + "'' " + img._getexif()[34853][3] + "\n")
                # file.write("\n")
                file.write(onlyfiles[i] + ", ")

                if img._getexif().get(306) is not None:
                    file.write(str(img._getexif()[306]) + ", ")
                if img._getexif().get(34853).get(2) is not None:
                    file.write(str(img._getexif()[34853][2][0][0]) + "° " + str(img._getexif()[34853][2][1][0]) + "' " + str(img._getexif()[34853][2][2][0] / img._getexif()[34853][2][2][1]) + "'' " + img._getexif()[34853][1] + ", ")
                if img._getexif().get(34853).get(4) is not None:
                    file.write(str(img._getexif()[34853][4][0][0]) + "° " + str(img._getexif()[34853][4][1][0]) + "' " + str(img._getexif()[34853][4][2][0] / img._getexif()[34853][4][2][1]) + "'' " + img._getexif()[34853][3] + ", ")
                file.write("\n")

            else:
                file.write(onlyfiles[i] + ", ")
                if img._getexif().get(306) is not None:
                    file.write(str(img._getexif()[306]) + ", ")
                    file.write("\n")

                print("NO DATA")
        else:
            file.write(onlyfiles[i])
            file.write("\n")
            print("NO DATA")

file.close()
