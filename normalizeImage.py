import numpy as np
from scipy.misc import imshow, imread
from PIL import Image


imgPath = '/home/aether/Desktop/Medical Image Segmentation/lung_unet_model/Lung_CT/train/images/ID_0000_Z_0142.png'

# open image into np array
# np_img = imread(imgPath)
img = Image.open(imgPath)
np_img = np.asarray(img)#[:,:,:3]
# print np_img.shape #(512,512,3)
print np.max(np_img), np.min(np_img)
imshow(np_img)


# data normalization
np_img = np_img.astype('float32')
mean = np.mean(np_img)
std = np.std(np_img)
np_img -= mean
np_img /= std
# print np_img.shape #(512,512,3)
print np.max(np_img), np.min(np_img)
imshow(np_img)

# conclusion - data normalization does not affect how the image looks
