import skimage.io as skio
import skimage as sk
import numpy as np
import os
from matplotlib import pyplot as plt
from PIL import Image
import warnings

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

def thresh_images(dir, save_dir):
	if not os.path.exists(save_dir):
		os.makedirs(save_dir)
	for filename in os.listdir(dir):
		print filename

		img_arr = skio.imread(dir + filename)[:,:,:3]
		# print img_arr.shape
		# print(np.max(img_arr))
		# print(np.min(img_arr))

		# ------- Make white/black ----------
		img_arr[img_arr > 0] = 255


		# ------- Labeling myocardium --------
		# if white(1) make black(0)
		# img_arr[img_arr == 1.0] = 0.0
		# if gray make white
		# img_arr[img_arr > 0.0] = 1.0
		# -----------------------------------

		# skio.imshow(img_arr)
		# skio.show()
		with warnings.catch_warnings():
			warnings.simplefilter("ignore")
			skio.imsave(save_dir + filename, img_arr)
		# break


for i in range(3, 131):
	thresh_images("/media/aether/My Passport/Medical Images Data/LITS - Liver Tumor Segmentation (perfect)/train_ground_truth_tumor/segmentation" + str(i) + "/"
			, "/media/aether/My Passport/Medical Images Data/LITS - Liver Tumor Segmentation (perfect)/train_ground_truth_binary/segmentation" + str(i) + "/")
