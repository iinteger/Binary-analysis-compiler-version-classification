import matplotlib.pyplot as plt
from pathlib import Path
import os
import re
import numpy as np

np.random.seed(0)
def load_data(img_size):
    version = [0, 0, 0, 0, 0, 0, 0]
    x_data=[]
    y_data=[]

    xAppend = x_data.append
    yAppend = y_data.append

    for p in Path("./Gather/").glob("**\\*."+"png"):  # binutils
        try:
            p = str(p).replace("\\", "/")
            file = plt.imread(p).copy()

            file.resize((img_size, img_size))

            xAppend(file)

            label = [0, 0, 0, 0, 0, 0, 0]

            label[int(p[10:11])-3] = 1
            version[int(p[10:11])-3] += 1

            yAppend(label)
        except:
            pass

    for p in Path("./Gather2/").glob("**\\*."+"png"):  # coreutils
        try:
            p = str(p).replace("\\", "/")
            file = plt.imread(p).copy()

            file.resize((img_size, img_size))

            xAppend(file)

            label = [0, 0, 0, 0, 0, 0, 0]
            label[int(p[11:12])-3] = 1
            version[int(p[11:12])-3] += 1

            yAppend(label)
        except:
            pass

    return x_data, y_data
