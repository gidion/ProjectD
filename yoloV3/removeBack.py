import sys
sys.version
import numpy as np
import os
import matplotlib.pyplot as plt
from PIL import Image,ImageOps


# import detect as det

imagePath = 'C:\\Users\\basro\\Desktop\\python_projects\\imageCombination\\images\\'
path = 'C:/Users/basro/Desktop/python_projects/imageCombination/images/person.jpeg'

clothingImg = plt.imread(imagePath + 'jurkk.png')



def makeBlack(clothingImg, row, p):
    clothingImg[row][p][0] = 0.
    clothingImg[row][p][1] = 0.
    clothingImg[row][p][2] = 0.
    clothingImg[row][p][3] = 1.
    return clothingImg


def colorCheck(rgb, clothingImgp):
    err_mar = 0.01

    for x in range(4):
        if clothingImgp[x] >= rgb[x] - 1*err_mar and  clothingImgp[x] <= rgb[x] + 1*err_mar:
            return True
        else:
            return False


def blackPixelCheck(row, p):
    if clothingImg[row][p][0] == 0. and clothingImg[row][p][1] == 0. and clothingImg[row][p][2] == 0. and clothingImg[row][p][3] == 1.:
        return True
    else:
        return False


def removeDupes(list):
        list = list(dict.fromkeys(list))
        return list




def prepClothingImg(clothingImg):

    plt.imshow(clothingImg)

    r = clothingImg[0][0][0]
    g = clothingImg[0][0][1]
    b = clothingImg[0][0][2]
    a = clothingImg[0][0][3]

    rgb = [r, g, b, a]

    clothingImg[0][0][0] = 0.
    clothingImg[0][0][1] = 0.
    clothingImg[0][0][2] = 0.
    clothingImg[0][0][3] = 0.

    rown = -1
    ppcounter = -1

    top = 10000
    right = 0
    left = 10000
    bottom = 0
    topCon = True

    for row in range(len(clothingImg)):
        for p in range(len(clothingImg[row])):
            if p != 0:
                if blackPixelCheck(row - 1, p) or blackPixelCheck(row, p - 1):
                    if colorCheck(rgb, clothingImg[row][p]):
                        clothingImg = makeBlack(clothingImg, row, p)
            else:
                if row != 0:
                    if blackPixelCheck(row - 1, p):
                        if colorCheck(rgb, clothingImg[row][p]):
                            clothingImg = makeBlack(clothingImg, row, p)

        for p in range(len(clothingImg[row])):
            if colorCheck(rgb, clothingImg[row][p]):
                if not(blackPixelCheck(row, p) and blackPixelCheck(row, p + 1)):
                    clothingImg = makeBlack(clothingImg, row, p)
                    for pn in range(p, 0, -1):
                        if not(blackPixelCheck(row, p)) and blackPixelCheck(row, p + 1):
                            clothingImg = makeBlack(clothingImg, row, p)

    for row in range(len(clothingImg)):
        for p in range(len(clothingImg[row])):
            try:
                #top coords
                if row != 0:
                    if not(blackPixelCheck(row, p)) and blackPixelCheck(row - 1, p):
                        if row < top:
                            top = row

                #left coords
                if row != 0:
                    if not(blackPixelCheck(row, p)) and blackPixelCheck(row, p - 1):
                        if p < left:
                            left = p

                #right coords
                if not(blackPixelCheck(row, p)) and blackPixelCheck(row, p + 1):
                    if p > right:
                        right = p

                #bottom coords
                if not(blackPixelCheck(row, p)) and blackPixelCheck(row + 1, p):
                    if row > bottom:
                        bottom = row
            except:
                pass

    croppedclothingImg = clothingImg[top:bottom, left:right, :]

    fig = plt.imshow(croppedclothingImg)
    plt.axis('off')
    fig.axes.get_xaxis().set_visible(False)
    fig.axes.get_yaxis().set_visible(False)
    plt.savefig(imagePath + 'dressTest.png', bbox_inches='tight', pad_inches = 0)



prepClothingImg(clothingImg)




# det.detectImg('images', 0.5, 0.5, path)




personImg = Image.open(imagePath + 'person.jpeg')
preppedClothingImg = Image.open(imagePath + 'dressTest.png')

preppedClothingImg = preppedClothingImg.convert("RGBA")
datas = preppedClothingImg.getdata()

newData = []
for item in datas:
    if item[0] == 0 and item[1] == 0 and item[2] == 0:
        newData.append((1, 1, 1, 0))
    else:
        newData.append(item)


preppedClothingImg.putdata(newData)
# preppedClothingImg.save(imagePath + 'dressTest.png', "PNG")
# preppedClothingImg = Image.open(imagePath + 'dressTest.png')



personArr = [[69.49650962536151, 79.81791745699368, 140.99271869659424, 228.86136964651251, 'person'], [78.0356437242948, 122.10518382145807, 128.42830503903903, 194.9306159386268, 'body'], [75.33036331030038, 189.65974213526798, 133.28479979588434, 236.2583573414729, 'legs'], [84.74981157596294, 70.43559657610379, 116.62381865428044, 110.12970671286949, 'head']]
# person=0 body=1 legs=2 head=3

headCenter = (personArr[3][2] - personArr[3][0]) // 2

height = (personArr[1][3] - personArr[1][1]) * 3
width = (personArr[0][2] - personArr[0][0])



PreppedClothingImg = preppedClothingImg.resize((int(width), int(height)))
PreppedClothingImg.save(imagePath + 'dressTest.png')
npcImg = Image.open(imagePath + 'dressTest.png')

left = personArr[0][0]
top = personArr[1][1] - ((personArr[1][1] - personArr[3][3]) // 2)

backimg = personImg.copy()
backimg.paste(npcImg, (int(left), int(top)), mask=npcImg)


backimg.save(imagePath + 'combinedImg.png')




























#white
