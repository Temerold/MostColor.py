# Imports
from __future__ import print_function
from __future__ import division
import binascii
import struct
from PIL import Image, ImageColor
import numpy as np
import scipy
import scipy.misc
import scipy.cluster
import os
import pathlib

from config import *

# import ctypes
# import ctypes
# ctypes.windll.kernel32.SetConsoleTitleW("MostColor")

# Window title

import os
clear = lambda: os.system("cls")



if promptRoot:
    root = input("Desired filepath>>> ")

if writeColorsToFile:
    cols = []

fileTypes = ['.png', '.jpg', '.bmp', '.webp', '.jpeg']

num = 0
exist = 0
failed = 0

for root, dirs, files in os.walk(root, topdown=False):
    for apa in files:
        if (apa.lower().endswith(tuple(fileTypes))): # Rules for files allowed to search
            exist += 1

# Major code ..... ;(
for root, dirs, files in os.walk(root, topdown=False):
    for name in [fi for fi in files if fi.lower().endswith(tuple(fileTypes))]:
        try:
            num += 1
            im = Image.open(root + "\\" + name)
            width, height = im.size
            if debug:
                print("\nFile #%s:" % (num) +
                        "\nFile Path: " + root +
                        "\nFile Name: " + name +
                        "\nReading image . . ." +
                        "\nImage size: " + str(width) + " x " + str(height))


            ar = np.asarray(im)
            shape = ar.shape
            try:
                ar = ar.reshape(np.product(
                    shape[:2]), shape[2]).astype(float)
            except:
                pass
            if debug:
                print("\nFinding clusters . . .")
            try:
                codes, dist = scipy.cluster.vq.kmeans(ar, 5)
            except:
                pass
            if debug:
                print("\nCluster centres:\n", codes)

            try:
                vecs, dist = scipy.cluster.vq.vq(ar, codes)
            except:
                pass
            counts, bins = np.histogram(vecs, len(codes))

            index_max = np.argmax(counts)
            peak = codes[index_max]

            color = binascii.hexlify(bytearray(int(c)
                                                for c in peak)).decode('ascii')
            if color == "00000000":
                try:
                    peak = codes[index_max - 1]
                except:
                    pass
                color = binascii.hexlify(
                    bytearray(int(c) for c in peak)).decode('ascii')

                if debug:
                    print("\nMost frequent color is %s (#%s)\n\n" %
                          (peak, color))

                img = Image.new("RGB", (width, height),
                                ImageColor.getrgb("#" + color))
                os.remove(root + "\\" + name)
                img.save(root + "\\" + name)
                # img.show() # don't - may crash computer***

                if writeColorsToFile:
                    cols.append("#" + color)
        except:
            print("Operation failed (%s)" % root + "\\" + name)
            failed += 1



if writeColorsToFile:
    try:
        cols = list(dict.fromkeys(cols))
        f = open("colors_hex.csv", 'w')
        f.truncate(0)
        for col in cols:
            try:
                f.write(col + '\n')
                print("\nAppended color to file.")
            except:
                print("\nCouldn't append color to file")
        f.close()
    except:
        print("\nCouldn't append colors to file.")


if promptStop:
    input("Completed %s/%s operations>>>" %
        (str(exist - failed), str(exist)))
