from cv2 import imread, bitwise_not, imshow, waitKey
import numpy as np


imgPath = '/media/aether/My Passport/Medical Images Data/Kaggle Finding and Measuring Lungs in CT Data/2d_images_png/ID_0000_Z_0142.png'
img = imread(imgPath)

# invert image
img_inv = bitwise_not(img)

imshow('img', img_inv)
waitKey(0)
