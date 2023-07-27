import cv2
import numpy as np
import glob
import os
 
dir_path = "./image/video/0temp/7combine"
dirs = os.listdir(dir_path)
dirs.sort()
img_array = []
for filename in dirs:
    print(filename)
    frame_path = os.path.join(dir_path, filename)
    img = cv2.imread(frame_path)
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)
 
 
out = cv2.VideoWriter('7combine.avi',cv2.VideoWriter_fourcc(*'DIVX'), 15, size)
 
for i in range(len(img_array)):
    out.write(img_array[i])
out.release()