import numpy as np
import cv2
from random import randint

th = 80
k = randint(1,12)


def Diff():
    """Это функция Diff,которая рассчитывает разницу между соседними коэффициентами.
        y  --  номер строки.
        x   --  номер столбца.
        diff -- исходная возвращаемая разница.
        DCT_block8x8 -- блок 8х8 коэффицентов.
    """

    if y % 2 == 0:
        if x % 2 == 0:
            diff = DCT_block8x8[y][x] - DCT_block8x8[y][x + 1]
        else:
            diff = DCT_block8x8[y][x] - DCT_block8x8[y + 1][x]
    else:
        if x % 2 == 0:
            diff = DCT_block8x8[y][x] - DCT_block8x8[y - 1][x]
        else:
            diff = DCT_block8x8[y][x] - DCT_block8x8[y][x - 1]
    return diff


def imageminus128():
    """
    Это функция imageminus128,которая отнимает от каждого бита исходного изображения 128.
           y  --  номер строки.
           x   --  номер столбца.
           imf -- исходное ихображение представленно в виде матрицы.
           height_img:width_img-- размер исходного изображения.
    """
    i = 0
    j = 0
    while i < height_img:
        while j < width_img:
            imf[i][j] = imf[i][j] + 128
            j += 1
        j = 0
        i += 1


img = cv2.imread("fvfvfvvf.jpg", 2)
height_img, width_img = img.shape[:2]
imf = np.float32(img)
width_wm=input("enter width of the WM:")
height_wm=input("enter height of the WM:")
wm = np.zeros((height_img, width_img), np.uint8)
iwm = np.float32(wm)

imageminus128()

i = 0
j = 0
ii = 0
jj = 0
while i < height_img:
    while j < width_img:
        # Блок 8х8 коэффицентов после ДКП.
        DCT_block8x8 = cv2.dct(imf[i:i + 8, j:j + 8])
        y = 0
        x = 0
        # Цикл проходится по блоку 8х8 и эспортирует ЦВЗ.
        while y < 8:
            while x < 8:
                if 3 < y + x < 9:
                    diff = Diff()
                    if diff >= th / 2 or ((diff >= -k) and (diff <= th / 2)) or diff <= k - th:
                        iwm[ii][jj] = 255
                    if diff >= th - k or ((diff <= k) and (diff >= -th / 2)) or diff <= -th / 2:
                        iwm[ii][jj] = 0
                    jj += 1
                    if jj == int(width_wm):
                        jj = 0
                        if ii <= int(height_wm)-2:
                            ii += 1
                x += 1
            x = 0
            y += 1
        j += 8
    j = 0
    i += 8

i = height_img - 1
j = width_img - 1
#Данный цикл преобразовывает ЦВЗ в исходное разрещение.
while i != 0:
    if iwm[i][j] == 255:
        break
    i += -1
    j += -1

sss = np.uint8(iwm[0:i + 2, 0:j + 2])


cv2.imwrite('image.jpg', sss)

