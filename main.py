import numpy as np
import cv2
th = 80
k = 12
z = 2  # Измение z приведет к надежному ЦВЗ, но снизит качество изображения.


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


def imageplus128():
    """
    Это функция imageplus128,которая прибавляет к каждому биту исходного изображения 128.
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


def watermarkbits():
    """
        Это функция watermarkbits,которая преобразует исходную матрицу ЦВЗ в двоичный вид.
                   y  --  номер строки.
                   x   --  номер столбца.
                   iwm -- исходный ЦВЗ представлен в виде матрицы.
                   height_wm:width_wm-- размер исходного ЦВЗ.
        """
    y = 0
    x = 0
    while y < height_wm:
        while x < width_wm:
            iwm[y][x] = int(round(iwm[y][x] / 255, 0))
            x += 1
        x = 0
        y += 1


img = cv2.imread("lena.png", 2)
height_img, width_img = img.shape[:2]
imf = np.float32(img)

wm = cv2.imread("wm.jpg", 2)
height_wm, width_wm = wm.shape[:2]
iwm = np.float16(wm)



imageminus128()
watermarkbits()

ii = 0
jj = 0
i = 0
j = 0
while i < height_img:
    while j < width_img:
        # Блок 8х8 коэффицентов после ДКП.
        DCT_block8x8 = cv2.dct(imf[i:i + 8, j:j + 8])
        # DCкоэффициент 8х8 блока.
        DC = DCT_block8x8[0][0]
        median = [DCT_block8x8[0][1], DCT_block8x8[1][0], DCT_block8x8[1][1], DCT_block8x8[0][2], DCT_block8x8[0][3],
                  DCT_block8x8[1][2], DCT_block8x8[2][1], DCT_block8x8[2][0], DCT_block8x8[3][0]]
        # Медиана девять коэффициентов, упорядоченные зигзагообразной последовательности.
        median = np.median(median)

        if 1000 < abs(DC) < 1:
            M = z * median
        else:
            M = z * ((DC - median) / DC)
        y = 0
        x = 0
        # Цикл проходится по блоку 8х8 и встраивает ЦВЗ.
        while y < 8:
            while x < 8:
                if 3 < y + x < 9:
                    # Разницу между соседними коэффициентами.
                    diff = Diff()
                    if ii == height_wm - 1 and jj == width_wm:
                        break
                    if jj == width_wm:
                        jj = 0
                        if ii <= height_wm - 2:
                            ii += 1
                    if iwm[ii][jj] == 1:
                        if diff >= th - k:
                            while diff >= th - k:
                                diff = Diff()
                                DCT_block8x8[y][x] += -M
                        elif (diff <= k) and (diff >= -th / 2):
                            while diff <= k:
                                diff = Diff()
                                DCT_block8x8[y][x] += M
                        elif diff <= -th / 2:
                            while diff >= -th - k:
                                diff = Diff()
                                DCT_block8x8[y][x] += -M
                    else:
                        if diff > th / 2:
                            while diff > th + k:
                                diff = Diff()
                                DCT_block8x8[y][x] += -M
                        elif (diff >= -k) and (diff <= th / 2):
                            while diff <= -k:
                                diff = Diff()
                                DCT_block8x8[y][x] += -M
                        elif diff <= k - th:
                            while diff >= -th + k:
                                diff = Diff()
                                DCT_block8x8[y][x] += +M
                    jj += 1
                x += 1
            x = 0
            y += 1
        # Возвращение Блок 8х8 коэффицентов в исходное состояние.
        imf[i:i + 8, j:j + 8] = cv2.idct(DCT_block8x8)
        j += 8
    j = 0
    i += 8

imageplus128()

sss = np.uint8(imf)
#
cv2.imwrite('fvfvfvvf.jpg', sss)

