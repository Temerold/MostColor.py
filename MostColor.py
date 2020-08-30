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

NUM_CLUSTERS = 5

##### CONFIG
root = 'A:\Viktigt\Mina program\MostColor' # Filepath to check if prompt_Root = True (use '\\' instead of '\')

prompt_Root = False # Program asks for path of images (True), or pre-set root (above) (False)
prompt_Stop = False # Program says it's done when done (True), or instant close (False)
#####


if prompt_Root == True:
    root = input("Desired filepath>>> ")
    
dots3 = ['.png', '.jpg', '.bmp', '.gif']
dots4 = ['.webp', '.jpeg']

for root, dirs, files in os.walk(root, topdown=False):
    for name in files:
        if name[-4:] in dots3 or name[-5:] in dots4:
            try:
                print("File Path: " + root)
                print("File Name: " + name)
                print("\nReading image . . .")
                im = Image.open(root + "\\" + name)
             
                width, height = im.size
                print("Image size: " + str(width) + " x " + str(height))

                if im.size >= (150, 150):
                    im = im.resize((150, 150))
                    print("Resized image to 150 x 150.")
                ar = np.asarray(im)
                shape = ar.shape
                try:
                    ar = ar.reshape(np.product(shape[:2]), shape[2]).astype(float)
                except:
                    pass

                print("\nFinding clusters . . .")
                try:
                    codes, dist = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)
                except:
                    pass
                print("\nCluster centres:\n", codes)

                try:
                    vecs, dist = scipy.cluster.vq.vq(ar, codes)
                except:
                    pass
                counts, bins = np.histogram(vecs, len(codes))


                index_max = np.argmax(counts)
                peak = codes[index_max]
                
                colour = binascii.hexlify(bytearray(int(c) for c in peak)).decode('ascii')
                if colour == "00000000":
                    try:
                        peak = codes[index_max - 1]
                    except:
                        pass
                    colour = binascii.hexlify(bytearray(int(c) for c in peak)).decode('ascii')
                print("\nMost frequent color is %s (#%s)" % (peak, colour))

                

                img = Image.new("RGB", (width, height), ImageColor.getrgb("#" + colour))
                os.remove(root + "\\" + name)
                img.save(root + "\\" + name)
                # img.show() # don't - may crash PC
            except:
                print("Operation failed (%s)" % root + "\\" + name)
                
    if prompt_Stop == True:
        input(">>>")
