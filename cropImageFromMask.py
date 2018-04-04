import cv2
import numpy as np
import os
import re

imgPath = '/home/aether/Desktop/Medical Image Segmentation/lung_unet_model/Lung_CT/test/images/VESSEL12_02_png/'
maskPath = '/home/aether/Desktop/Medical Image Segmentation/lung_unet_model/Lung_CT/test/ground_truth/VESSEL12_02_png/'
croppedPath = 'VESSEL12_02_perfect_cropped/'

if not os.path.exists(croppedPath):
    os.makedirs(croppedPath)

# Test if a given chunk is an int
def tryint(c):
    try:
        return int(c)
    except:
        return c

# turn a string into a list of string and number chunks
def alphanum_key(s):
    return [tryint(c) for c in re.split('([0-9]+)', s)]

# sort the given list
def natural_sort(list):
    list.sort(key=alphanum_key)

allImgPaths = []
allMaskPaths = []

# Loop through the folders and save full paths of each image
for path, subdirs, files in os.walk(imgPath):
    natural_sort(files)
    for imgFile in files:
        allImgPaths.append(path + imgFile)

for path, subdirs, files in os.walk(maskPath):
    natural_sort(files)
    for maskFile in files:
        allMaskPaths.append(path + maskFile)

assert (len(allImgPaths) == len(allMaskPaths))
combinePaths = zip(allImgPaths, allMaskPaths)

count = 0
for imgFile, maskFile in combinePaths:
    img = cv2.imread(imgFile)
    mask = cv2.imread(maskFile, 0)
    print imgFile
    # print img.shape
    # print mask.shape

    # Crop out image from mask with bitwise_and operation
    # mask_out = cv2.subtract(mask, img)
    # mask_out = cv2.subtract(mask, mask_out)
    mask_out = cv2.bitwise_and(img, img, mask=mask)
    # print mask_out.shape

    # cv2.imshow('img', mask_out)
    # cv2.waitKey(0)

    cv2.imwrite(croppedPath + "slice" + str(count) + ".png", mask_out)
    count += 1
