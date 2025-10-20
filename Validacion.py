import random as random
from PIL import Image
import numpy as np
imagen = Image.open('ImagenesPython')
paths = ["1.jpg", "2.jpg", "3.jpg", "4.jpg",
         "5.jpg", "6.jpg", "7.jpg", "8.jpg",
         "9.jpg", "10.jpg", "11.jpg", "12.jpg",
         "13.jpg", "14.jpg", "15.jpg"]
pares_paths = paths*2
random.shuffle(pares_paths)
tablero = np.full((5, 6), "", dtype=str)
index = 0
for i in range(len(tablero)):
    for j in range(len(tablero[i])):
        tablero[i][j] = pares_paths[index]
        index = index + 1

print(tablero)
